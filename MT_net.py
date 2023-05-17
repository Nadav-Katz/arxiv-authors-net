import json
import pandas as pd
from collections import defaultdict
from queue import Queue
from threading import Thread
from datetime import datetime
from tqdm import tqdm


class ArxivDataGenerator:
    def __init__(self, filename, max_rows=None, chunk_size=1000):
        self.filename = filename
        self.max_rows = max_rows
        self.chunk_size = chunk_size

    def __iter__(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines_processed = 0
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


# class AuthorsNetwork:
#     def __init__(self, filename, max_rows=None, chunk_size=1000):
#         self.data_generator = ArxivDataGenerator(filename, max_rows=max_rows, chunk_size=chunk_size)
#         self.max_rows = max_rows
#         self.queue = Queue()
#         self.network_dict = defaultdict(list)
#         self.network_df = None
#         self.num_producers = 2
#         self.num_consumers = 4

#     def _process_data(self, data):
#         for paper in data:
#             authors = paper['authors_parsed']
#             paper_date = [v['created'] for v in paper['versions']]
#             dt = [datetime.strptime(d, '%a, %d %b %Y %H:%M:%S %Z') for d in paper_date]
#             paper_date = max(dt).strftime('%d/%m/%Y') if dt else None

#             for i in range(len(authors)):
#                 for j in range(i + 1, len(authors)):
#                     author1 = tuple(authors[i])
#                     author2 = tuple(authors[j])
#                     if author1 != author2:
#                         # update paper count for the author pair
#                         self.queue.put((author1, author2, paper['id'], paper_date))
    
#     def _produce_data(self):
#         for data in self.data_generator:
#             self._process_data(data)


#     def _consume_data(self):
#         while not self.queue.empty() or not all(p.is_alive() for p in self.producers):
#             try:
#                 author1, author2, paper_id, paper_date = self.queue.get(timeout=1)
#                 if (author1, author2) in self.network_dict and not paper_id in self.network_dict[(author1, author2)]['paper_ids']:
#                     self.network_dict[(author1, author2)]['paper_ids'].append(paper_id)
#                     self.network_dict[(author1, author2)]['paper_dates'].append(paper_date)
#                 else:
#                     self.network_dict[(author1, author2)] = {'paper_ids': [paper_id], 'paper_dates': [paper_date]}
#             except:
#                 continue
    
#     def build_network_df(self):
#         self.producers = [Thread(target=self._produce_data) for _ in range(self.num_producers)]
#         self.consumers = [Thread(target=self._consume_data) for _ in range(self.num_consumers)]
        
#         for p in self.producers:
#             p.start()
#         for c in self.consumers:
#             c.start()
#         for p in self.producers:
#             p.join()
#         for c in self.consumers:
#             c.join()
        
#         network_dict = {'author1': [], 'author2': [], 'paper_ids': [], 'paper_dates': []}
#         for (author1, author2), papers_info in self.network_dict.items():
#             network_dict['author1'].append(author1)
#             network_dict['author2'].append(author2)
#             network_dict['paper_ids'].append(papers_info['paper_ids'])
#             network_dict['paper_dates'].append(papers_info['paper_dates'])

#         self.network_df = pd.DataFrame(network_dict)
#         return self.network_df

#     def to_networkx(self):
#         G = nx.Graph()
#         for _, row in self.network_df.iterrows():
#             author1 = row['author1']
#             author2 = row['author2']
#             weight = len(row['paper_ids'])
#             G.add_edge(author1, author2, weight=weight)
#         return G

### working!!

# class AuthorsNetwork:
#     def __init__(self, filename, max_rows=None, chunk_size=1000):
#         self.data_generator = ArxivDataGenerator(filename, max_rows=max_rows, chunk_size=chunk_size)
#         self.max_rows = max_rows
#         self.queue = Queue()
#         self.network_dict = defaultdict(list)
#         self.network_df = None
#         self.num_producers = 2
#         self.num_consumers = 4

#     def _process_data(self, data):
#         for paper in data:
#             authors = paper['authors_parsed']
#             paper_date = [v['created'] for v in paper['versions']]
#             dt = [datetime.strptime(d, '%a, %d %b %Y %H:%M:%S %Z') for d in paper_date]
#             paper_date = max(dt).strftime('%d/%m/%Y') if dt else None

#             for i in range(len(authors)):
#                 for j in range(i + 1, len(authors)):
#                     author1 = tuple(authors[i])
#                     author2 = tuple(authors[j])
#                     if author1 != author2:
#                         # update paper count for the author pair
#                         self.queue.put((author1, author2, paper['id'], paper_date))

#     def _produce_data(self):
#         for data in self.data_generator:
#             self._process_data(data)

#     def _consume_data(self):
#         while True:
#             try:
#                 author1, author2, paper_id, paper_date = self.queue.get(timeout=1)
#                 if (author1, author2) in self.network_dict:
#                     index = next(
#                         (
#                             idx
#                             for idx, p_id in enumerate(self.network_dict[(author1, author2)]['paper_ids'])
#                             if p_id == paper_id
#                         ),
#                         None
#                     )
#                     if index is None:
#                         self.network_dict[(author1, author2)]['paper_ids'].append(paper_id)
#                         self.network_dict[(author1, author2)]['paper_dates'].append(paper_date)
#                 else:
#                     self.network_dict[(author1, author2)] = {'paper_ids': [paper_id], 'paper_dates': [paper_date]}
#             except:
#                 break

#     def build_network_df(self):
#         self.producers = [Thread(target=self._produce_data) for _ in range(self.num_producers)]
#         self.consumers = [Thread(target=self._consume_data) for _ in range(self.num_consumers)]

#         for p in self.producers:
#             p.start()
#         for c in self.consumers:
#             c.start()
#         for p in self.producers:
#             p.join()
#         for c in self.consumers:
#             c.join()

#         network_dict = {'author1': [], 'author2': [], 'paper_ids': [], 'paper_dates': []}
#         for (author1, author2), papers_info in self.network_dict.items():
#             network_dict['author1'].append(author1)
#             network_dict['author2'].append(author2)
#             network_dict['paper_ids'].append(papers_info['paper_ids'])
#             network_dict['paper_dates'].append(papers_info['paper_dates'])

#         self.network_df = pd.DataFrame(network_dict)
#         return self.network_df




class AuthorsNetwork:
    def __init__(self, filename, max_rows=None, chunk_size=1000):
        self.data_generator = ArxivDataGenerator(filename, max_rows=max_rows, chunk_size=chunk_size)
        self.max_rows = max_rows
        self.queue = Queue()
        self.network_dict = defaultdict(list)
        self.network_df = None
        self.num_producers = 1
        self.num_consumers = 4

    def _process_data(self, data, progress_bar):
        for i, paper in enumerate(data):
            authors = paper['authors_parsed']
            paper_date = [v['created'] for v in paper['versions']]
            dt = [datetime.strptime(d, '%a, %d %b %Y %H:%M:%S %Z') for d in paper_date]
            paper_date = [d.strftime('%d/%m/%Y') for d in dt]
            paper_date = max(paper_date)

            for i in range(len(authors)):
                for j in range(i + 1, len(authors)):
                    author1 = tuple(authors[i])
                    author2 = tuple(authors[j])
                    if author1 != author2:
                        # update paper count for the author pair
                        self.queue.put((author1, author2, paper['id'], paper_date))
            
            if i % self.num_producers == 0:
                progress_bar.update(1)
            
            

    def _produce_data(self, progress_bar):
        for data in self.data_generator:
            self._process_data(data, progress_bar)

    
    def _consume_data(self, progress_bar):
        while True:
            try:
                author1, author2, paper_id, paper_date = self.queue.get(timeout=1)
                if (author1, author2) in self.network_dict:
                    index = next(
                        (
                            idx
                            for idx, p_id in enumerate(self.network_dict[(author1, author2)]['paper_ids'])
                            if p_id == paper_id
                        ),
                        None
                    )
                    if index is None:
                        self.network_dict[(author1, author2)]['paper_ids'].append(paper_id)
                        self.network_dict[(author1, author2)]['paper_dates'].append(paper_date)
                else:
                    self.network_dict[(author1, author2)] = {'paper_ids': [paper_id], 'paper_dates': [paper_date]}
            except:
                break
            # progress_bar.update(1)

    def build_network_df(self):
        total_papers = self.max_rows if self.max_rows is not None else "Unknown"
        progress_bar = tqdm(total=total_papers, desc="Creating network")

        self.producers = [Thread(target=self._produce_data, args=(progress_bar,)) for _ in range(self.num_producers)]
        self.consumers = [Thread(target=self._consume_data, args=(progress_bar,)) for _ in range(self.num_consumers)]

        for p in self.producers:
            p.start()
        for c in self.consumers:
            c.start()
        for p in self.producers:
            p.join()
        for c in self.consumers:
            c.join()

        progress_bar.close()

        network_dict = {'author1': [], 'author2': [], 'paper_ids': [], 'paper_dates': []}
        for (author1, author2), papers_info in self.network_dict.items():
            network_dict['author1'].append(author1)
            network_dict['author2'].append(author2)
            network_dict['paper_ids'].append(papers_info['paper_ids'])
            network_dict['paper_dates'].append(papers_info['paper_dates'])

        self.network_df = pd.DataFrame(network_dict)
        return self.network_df

    def to_networkx(self):
        G = nx.Graph()
        for _, row in self.network_df.iterrows():
            author1 = row['author1']
            author2 = row['author2']
            weight = len(row['paper_ids'])
            G.add_edge(author1, author2, weight=weight)
        return G