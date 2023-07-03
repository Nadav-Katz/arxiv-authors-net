from authors_net.builder import AuthorsNetwork
import pandas as pd 
import networkx as nx


# create net: 
network_nt = AuthorsNetwork(filename='arxiv-metadata-oai-snapshot.json',
                                max_rows=None,
                                chunk_size=1000,
                                extra_edge_features=False, 
                                num_workers=2)
# create network:
df = network_nt.build_network_df()

# some interesting cases: 
df.sort_values(by='paper_count', ascending=False).head(10)

# convert to graph: 
g = network_nt.to_networkx()

# interesting measures:
g.number_of_edges()
g.number_of_nodes()
nx.number_connected_components(g)
nx.katz_centrality(g)