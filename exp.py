# from network import AuthorsNetwork as Reg
from MT_net import AuthorsNetwork as MT

# create net: 
# network_reg = Reg(filename='arxiv-metadata-oai-snapshot.json', max_rows=10000)
network_nt = MT(filename='arxiv-metadata-oai-snapshot.json', max_rows=None, chunk_size=1000)

# demo:
# df_reg = network_reg.build_network_df()
df = network_nt.build_network_df()

# print(df_reg.shape)
print(df.shape)


df['len'] = df['paper_ids'].transform(len)
df.sort_values(by='len', ascending=False).head(10)




# import pandas as pd 

# pd.to_pickle(df, "colab_net.pkl", compression='gzip')