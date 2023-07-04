# Arxiv co-authorship network
The goal of this repository, is to provide a way to create an undirected network of authors, where each node represents an author, and each edge represents a co-authorship relation. Each edge is weighted by the number of papers written together by the connected authors, and some extra edge features such as paper id and the latest version upload date to Arxiv are also available. 

To address the space and time that takes to process the vast amount of data in this dataset, and to speed things up a little, we used multi-threading, implemented according to the "producer-consumer" design pattern, which potentially uses more than one core with multi processes, and addresses the problems rises using multi-threading in such scenarios.
 
## installation:
```
pip install git+https://github.com/Nadav-Katz/arxiv-authors-net.git#egg=AuthorsNet
```

## How to use:
The input file to the builder should be the original Arxiv dataset from kaggle, or one with identical structure (a subset for example).
To create the network from the entire file, use `max_rows=None`.
In order to create a network with some edge features, such as Arxiv paper id and last upload date, use `extra_edge_features=True`.

```python
from authors_net.builder import AuthorsNetwork
import pandas as pd 

# define the network creator object:
network = AuthorsNetwork(filename='arxiv-metadata-oai-snapshot.json',
                         max_rows=10000,
                         chunk_size=1000,
                         extra_edge_features=False,
                         num_workers=2)

# create network edge list (DataFrame):
df = network.build_network_df()


```
While working, a folder named `network_data_files` is automatically created. the network generator saves checkpoints while generating, so if for some reason the code stopped, all you need to do is create an instance of `AuthorsNetwork` class, with the argument `resume=True`. when activated, the builder will look for the folder created with the previous builder, and will resume the process from the last paper processed: 
```python
network = AuthorsNetwork(filename='arxiv-metadata-oai-snapshot.json',
                         max_rows=10000,
                         chunk_size=1000,
                         extra_edge_features=False,
                         num_workers=2,
                         resume=True)

``` 
You can also convert the network into `networkx` graph object for further analysis (may take some time):

```python
G = network.to_networkx()
```
