from authors_net.builder import AuthorsNetwork
import pandas as pd 
import networkx as nx

# create net: 
network_nt = AuthorsNetwork(filename='arxiv-metadata-oai-snapshot.json',
                            max_rows=None,
                            chunk_size=100,
                            extra_edge_features=False, 
                            num_consumers=1, num_producers=1)
# create network:
df = network_nt.build_network_df()

# write to pkl:
pd.to_pickle(df, "colab_net.pkl", compression='gzip')

print(df.shape)

# some interesting cases: 
df.sort_values(by='paper_count', ascending=False).head(10)

# convert to graph: 
g = network_nt.to_networkx()

print(f'The network has {len(g.edges)} edges and {len(g.nodes)} nodes')