from network import AuthorsNetwork

# create net: 
network = AuthorsNetwork(filename='arxiv-metadata-oai-snapshot.json', max_rows=20)

# demo as df:
df = network.build_network_df()
print(df.head(100))
