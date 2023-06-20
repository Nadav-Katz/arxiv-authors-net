from dataclasses import dataclass
import json
import networkx as nx
from datetime import datetime
import pandas as pd
from collections import defaultdict
from typing import List, Dict, Any
from tqdm import tqdm


class ArxivDataGenerator:
    def __init__(self, filename, max_rows=None):
        self.filename = filename
        self.max_rows = max_rows

    def __iter__(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if self.max_rows is not None and i >= self.max_rows:
                    break
                paper = json.loads(line)
                yield paper


class AuthorsNetwork:
    def __init__(self, filename, max_rows=None):
        self.data_generator = ArxivDataGenerator(filename, max_rows=max_rows)
        self.network_df = None
    
    def build_network_df(self):
        network_dict = {'author1': [], 'author2': [], 'paper_ids': [], 'paper_dates': []}
        paper_ids = defaultdict(list)  # dictionary to keep track of paper ids
        paper_dates = defaultdict(list)

        for paper in tqdm(self.data_generator):
            # paper = Paper(**line)
            paper_id = paper['id']
            # paper_id = paper.id 
            paper_date = [v['created'] for v in paper['versions']]
            # paper_date = [v['created'] for v in paper.versions]
            dt = [datetime.strptime(d, '%a, %d %b %Y %H:%M:%S %Z') for d in paper_date]  
            paper_date = [d.strftime('%d/%m/%Y') for d in dt]
            paper_date = max(paper_date)
            authors = paper['authors_parsed']
            # authors = paper.authors
            
            for i in range(len(authors)):
                for j in range(i+1, len(authors)):
                    author1 = tuple(authors[i])
                    author2 = tuple(authors[j])
                    if author1 != author2:
                        # update paper ids for the author pair
                        paper_ids[(author1, author2)].append(paper_id)
                        paper_dates[(author1, author2)].append(paper_date)


        # add edges to network_dict based on paper ids
        for ids, dates in zip(paper_ids.items(), paper_dates.items()):
            (author1, author2), id_p = ids
            (_, _), date_p = dates           
            network_dict['author1'].append(author1)
            network_dict['author2'].append(author2)
            network_dict['paper_ids'].append(id_p)
            network_dict['paper_dates'].append(date_p)

        network_df = pd.DataFrame(network_dict)
        return network_df

    def to_networkx(self):
        G = nx.Graph()
        for _, row in self.network_df.iterrows():
            author1 = row['author1']
            author2 = row['author2']
            paper_ids = row['paper_ids']
            G.add_edge(author1, author2, papers=paper_ids)
        return G
    

############################

# ## old version: 
# net = AuthorsNetwork(filename='arxiv-metadata-oai-snapshot.json')
# df_1 = net.build_network_df()

# pd.to_pickle(df_1, "colab_net.pkl", compression='gzip')
