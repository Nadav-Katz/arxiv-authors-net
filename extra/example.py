from authors_net.builder import AuthorsNetwork
import pandas as pd 
import networkx as nx


# create net: 
network_nt = AuthorsNetwork(filename='arxiv-metadata-oai-snapshot.json',
                                max_rows=10000,
                                chunk_size=1000,
                                extra_edge_features=False, 
                                num_workers=2)
# create network:
df = network_nt.build_network_df()

# write to pkl:
pd.to_pickle(df, "colab_net.pkl", compression='gzip')

# # some interesting cases: 
# df.sort_values(by='paper_count', ascending=False).head(10)

# # convert to graph: 
# g = network_nt.to_networkx()

# print(f'The network has {len(g.edges)} edges and {len(g.nodes)} nodes')