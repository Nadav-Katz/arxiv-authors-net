# Arxiv co-authorship network
The goal of this repository, is to provide a way to create an undirected network of authors, where each node represents an author, and each edge represents a co-authorship relation. Each edge is weighted by the number of papers written together by the connected authors, and extra features such as paper id and the upload date to Arxiv are also available. 

To address the space and time takes to process the vast amount of data in this dataset, and to speed things up a little, we used multi-threading, implemented according to the "producer-consumer" design pattern, which helps to address the problems rises using multi-threding in such problems.
 
## installation:
```
pip install git+https://github.com/Nadav-Katz/arxiv-authors-net.git#egg=AuthorsNet
```

## How to use:
A short example of how to use the code to build the network:
To create a net from the entire file, use `max_rows=None`.
In order to create a network with some edge features, such as paper arxiv id and dates, use `extra_edge_features=True`.

You can of course replace the filename with any file that matches the structure of the original network file from Kaggle.
```python
from authors_net.builder import AuthorsNetwork
import pandas as pd 

# define the network creator object:
network = AuthorsNetwork(filename='arxiv-metadata-oai-snapshot.json', 
                         max_rows=None,
                         chunk_size=100,
                         extra_edge_features=False, 
                         num_consumers=3, num_producers=1)

# create network edge list (DataFrame):
df = network.build_network_df()

# write to pkl:
pd.to_pickle(df, "colab_net.pkl", compression='gzip')
```
you can also convert the network into networkx graph object (takes some time):

```python
G = network.to_networkx()
```
