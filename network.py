import json
# import networkx as nx
from datetime import datetime
import pandas as pd
from collections import defaultdict


def read_arxiv_data(filename):
    with open(filename) as f:
        for line in f:
            paper = json.loads(line)
            authors = paper.get('authors_parsed', [])
            versions = paper.get('versions', [])
            doi = paper.get('doi')
            yield paper['id'], doi, authors, versions



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
        network_dict = {'author1': [], 'author2': [], 'paper_count': []}
        paper_count = defaultdict(int)  # dictionary to keep track of paper counts

        for paper in self.data_generator:
            authors = paper['authors_parsed']
            for i in range(len(authors)):
                for j in range(i+1, len(authors)):
                    author1 = tuple(authors[i])
                    author2 = tuple(authors[j])
                    if author1 != author2:
                        # update paper count for the author pair
                        paper_count[(author1, author2)] += 1

        # add edges to network_dict based on paper count
        for (author1, author2), count in paper_count.items():
            network_dict['author1'].append(author1)
            network_dict['author2'].append(author2)
            network_dict['paper_count'].append(count)

        network_df = pd.DataFrame(network_dict)
        return network_df
        
    
    def to_networkx(self):
        G = nx.Graph()
        G.add_weighted_edges_from(self.network_df.values)
        return G
    

############################

