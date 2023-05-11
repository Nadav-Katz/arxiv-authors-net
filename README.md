# arxiv-authors-net
This repository provides the code to build an authors collaboration network from the [Arxiv Dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv)
## Usage:
To present for example, the basic network for the first 100 papers: 
```python
from network import AuthorsNetwork

# create net: 
network = AuthorsNetwork(filename='arxiv-metadata-oai-snapshot.json', max_rows=100)

# present as df:
df = network.build_network_df()
print(df.head(100))
```

