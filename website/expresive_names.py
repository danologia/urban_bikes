import pandas as pd
import json 
import numpy as np

nodes = pd.read_csv("dane/stations_names.csv")
edges = pd.read_csv("dane/edge_with_weights.csv")


data = pd.merge(edges, nodes, how='left', left_on='source', right_on='id')
data = pd.merge(data, nodes, how='left', left_on='target', right_on='id', suffixes=['_source', '_target'])

data = data[['name_source', 'name_target', 'weight']].rename({'name_source': 'source', 'name_target': 'target'}, axis=1)

data.to_csv('dane/named_connections.csv', index=False)