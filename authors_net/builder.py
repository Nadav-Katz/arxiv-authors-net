import json
import pandas as pd
from collections import defaultdict
from multiprocessing import Manager
from datetime import datetime
from tqdm import tqdm
import networkx as nx
import concurrent.futures
import os


class ArxivDataGenerator:
    def __init__(self, file_path, max_rows=None, chunk_size=1000):
        self.file_path = file_path
        self.max_rows = max_rows
        self.chunk_size = chunk_size
        self.lines_to_skip = 0


    def __iter__(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines_processed = 0
            lines_skipped = 0

            # Skip rows if necessary
            while lines_skipped < self.lines_to_skip:
                f.readline()
                lines_skipped += 1
            
            while True:
                lines = []
                for i in range(self.chunk_size):
                    line = f.readline()
                    if not line or (self.max_rows is not None and lines_processed >= self.max_rows):
                        break
                    lines.append(line)
                    lines_processed += 1
                if lines:
                    yield [json.loads(line) for line in lines]
                else:
                    break
                     
    def __next__(self):
        next(iter(self))


class AuthorsNetwork:
    def __init__(self, filename, max_rows=None, chunk_size=1000, extra_edge_features=False, num_workers=2, resume=False):
        self.data_generator = ArxivDataGenerator(filename, max_rows=max_rows, chunk_size=chunk_size)
        self.max_rows = max_rows
        self.queue = Manager().Queue()
        self.network_dict = defaultdict(list)
        self.network_df = None
        self.num_producers = 1
        self.num_consumers = num_workers
        self.extra_edge_features = extra_edge_features
        self.output_folder = 'network_data_files'
        self.file_count = 0
        
        if resume:
            self.resume_from_checkpoint()
            self.file_count = len([file for file in os.listdir(self.output_folder) if "merged" not in file])


    def resume_from_checkpoint(self):
        rows_file_path = os.path.join(self.output_folder, 'rows_processed.txt')

        # Read the existing rows processed count
        existing_rows_processed = 0
        if os.path.exists(rows_file_path):
            with open(rows_file_path, 'r') as rows_file:
                existing_rows_processed = int(rows_file.read())
        
        self.data_generator.lines_to_skip = existing_rows_processed
    

    def _process_data(self, data, progress_bar):
        for idx, paper in enumerate(data):
            authors = paper['authors_parsed']
            paper_date = [v['created'] for v in paper['versions']]
            dt = [datetime.strptime(d, '%a, %d %b %Y %H:%M:%S %Z') for d in paper_date]
            paper_date = [k.strftime('%d/%m/%Y') for k in dt]
            paper_date = max(paper_date)
            paper_id = paper['id']

            for i in range(len(authors)):
                for j in range(i + 1, len(authors)):
                    author1 = tuple(authors[i])
                    author2 = tuple(authors[j])
                    if author1 != author2:
                        # update paper count for the author pair
                        self.queue.put((author1, author2, paper_id, paper_date))

            if idx % self.num_producers == 0:
                progress_bar.update(1)

    
    def _produce_data(self, progress_bar):
        for data in self.data_generator:
            self._process_data(data, progress_bar)

    def _consume_data(self):
        while True:
            try:
                author1, author2, paper_id, paper_date = self.queue.get(timeout=1)
                if author1 > author2:
                    # Swap authors if author1 > author2
                    author1, author2 = author2, author1
                if (author1, author2) in self.network_dict.keys():
                    if self.extra_edge_features:
                        ind = next(
                            (
                                idx
                                for idx, p_id in enumerate(self.network_dict[(author1, author2)]['paper_ids'])
                                if p_id == paper_id
                            ),
                            None)

                        if ind is None:
                            self.network_dict[(author1, author2)]['paper_ids'].append(paper_id)
                            self.network_dict[(author1, author2)]['paper_dates'].append(paper_date)
                    self.network_dict[(author1, author2)]['paper_count'] += 1  # Update paper count
                else:
                    if self.extra_edge_features:
                        self.network_dict[(author1, author2)] = {'paper_ids': [paper_id], 'paper_dates': [paper_date], 'paper_count': 1}
                    else:
                        self.network_dict[(author1, author2)] = {'paper_count': 1}
            except:
                break
    
    def _save_network_df(self, rows_processed):
        if self.extra_edge_features:
            network_dict = {'author1': [], 'author2': [], 'paper_ids': [], 'paper_dates': [], 'paper_count': []}
        else:
            network_dict = {'author1': [], 'author2': [], 'paper_count': []}

        # Create a copy of the network dictionary
        network_dict_copy = dict(self.network_dict)

        for (author1, author2), papers_info in network_dict_copy.items():
            network_dict['author1'].append(str(author1))
            network_dict['author2'].append(str(author2))

            if self.extra_edge_features:
                network_dict['paper_ids'].append(papers_info['paper_ids'])
                network_dict['paper_dates'].append(papers_info['paper_dates'])

            network_dict['paper_count'].append(papers_info['paper_count'])  # Add paper count to the network dictionary

        network_df = pd.DataFrame(network_dict)

        # Save network data to file
        os.makedirs(self.output_folder, exist_ok=True)
        file_name = f'network_data_{self.file_count}.pickle'
        file_path = os.path.join(self.output_folder, file_name)
        network_df.to_pickle(file_path)

        # Update the rows processed count in the existing file
        rows_file_path = os.path.join(self.output_folder, 'rows_processed.txt')

        # Read the existing rows processed count
        existing_rows_processed = 0
        if os.path.exists(rows_file_path):
            with open(rows_file_path, 'r') as rows_file:
                existing_rows_processed = int(rows_file.read())

        # Add the new rows processed to the existing count
        total_rows_processed = existing_rows_processed + rows_processed

        # Update the rows processed count in the file
        with open(rows_file_path, 'w') as rows_file:
            rows_file.write(str(total_rows_processed))

        self.file_count += 1

        # Clear network dictionary for the next file
        self.network_dict.clear()

    def _clear_memory(self):
        self.network_dict.clear()
        self.queue = Manager().Queue()

    def _merge_network_files(self):
        files = [file for file in os.listdir(self.output_folder) if file.endswith('.pickle') and not "merged" in file]
        dfs = []

        for file in files:
            file_path = os.path.join(self.output_folder, file)
            df = pd.read_pickle(file_path)
            dfs.append(df)

        if len(dfs) > 1:
            self.network_df = pd.concat(dfs, ignore_index=True)
            if self.extra_edge_features:
                self.network_df = self.network_df.groupby(['author1', 'author2'], as_index=False).agg({
                    'paper_ids': lambda x: sum(x, []),
                    'paper_dates': lambda x: sum(x, []),
                    'paper_count': 'sum'
                })
                            # Convert paper_ids and paper_dates columns to lists
                self.network_df['paper_ids'] = self.network_df['paper_ids'].apply(lambda x: [] if pd.isna(x) else x)
                self.network_df['paper_dates'] = self.network_df['paper_dates'].apply(lambda x: [] if pd.isna(x) else x)
            else:
                self.network_df = self.network_df.groupby(['author1', 'author2'], as_index=False).agg({
                    'paper_count': 'sum'
                })
                

        elif len(dfs) == 1:
            self.network_df = dfs[0]
        else:
            self.network_df = pd.DataFrame()

        # Save final merged network data to file
        merged_file_path = os.path.join(self.output_folder, 'network_data_merged.pickle')
        self.network_df.to_pickle(merged_file_path)

    def build_network_df(self):
        total_papers = self.max_rows if self.max_rows is not None else 2231517
        progress_bar = tqdm(total=total_papers, desc="Creating network")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_consumers) as executor:
            futures = [executor.submit(self._consume_data) for _ in range(self.num_consumers)]

            for data in self.data_generator:
                self._process_data(data, progress_bar)
                if progress_bar.n % 10000 == 0:
                    self._save_network_df(rows_processed=progress_bar.n)
                    self.network_dict.clear()

            for future in concurrent.futures.as_completed(futures):
                future.result()

        progress_bar.close()

        self._save_network_df(rows_processed=progress_bar.n)
        self._merge_network_files()

        return self.network_df
    
    
    def to_networkx(self):
        G = nx.Graph()
        for _, row in tqdm(self.network_df.iterrows(), desc='Converting to NetworkX', total=self.network_df.shape[0]):
            author1 = row['author1']
            author2 = row['author2']
            weight = row['paper_count']
            if self.extra_edge_features:
                attrs = row['paper_ids'], row['paper_dates']
                G.add_edge(author1, author2, weight=weight, attr=attrs)
            else:
                G.add_edge(author1, author2, weight=weight)

        return G

