from authors_net.builder import AuthorsNetwork
import pandas as pd 

# create net: 
network_nt = AuthorsNetwork(filename='arxiv-metadata-oai-snapshot.json', max_rows=None, chunk_size=10)

# create network:
df = network_nt.build_network_df()

print(df.shape)


df['len'] = df['paper_ids'].transform(len)
df.sort_values(by='len', ascending=False).head(10)


# write to pkl:
pd.to_pickle(df, "colab_net.pkl", compression='gzip')