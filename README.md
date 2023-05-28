# Arxiv co-authorship network
The goal of this repo, is to provide a way to create an undirected network of authors, where each
node represents an author, and each edge represents a co-authorship relation. each edge containes a list of papers id's written together by the connected authors, and the date they where uploaded to Arxiv. 

To address the space and time that processing this vast amount of data in this dataset takes, and to speed things up, we used multi-threading, implemented according to the "producer-consumer" design pattern, sutiable to address this kind of problems.
 
## installation:
```
pip install git+https://github.com/Nadav-Katz/arxiv-authors-net.git#egg=AuthorsNet
```

## How to use:
A short example of how to use the code to build the network:
To create a net from the entire file, use `max_rows=None`.
You can of course replace the filename with any file that matches the structure of the original network file from Kaggle.
```python
from authors_net.builder import AuthorsNetwork
import pandas as pd 

# define the network creator object: 
network = AuthorsNetwork(filename='arxiv-metadata-oai-snapshot.json', max_rows=None, chunk_size=1000)

# create network:
df = network.build_network_df()

# write to pkl:
pd.to_pickle(df, "colab_net.pkl", compression='gzip')
```

you can also convert the network into networkx graph object (takes time):
```python
G = network.to_networkx()
```
