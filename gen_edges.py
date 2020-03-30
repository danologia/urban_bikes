import pandas as pd

nodes = pd.read_csv("dane/stations_names.csv")
edges = pd.read_csv("dane/edge_with_weights.csv")

edges = pd.merge(edges, nodes[["lat", "lng", "id"]], left_on='source', right_on='id', how="left").drop(["id"], axis=1)
edges = pd.merge(edges, nodes[["lat", "lng", "id"]], left_on='target', suffixes=("_source", "_target"), right_on='id', how="left").drop(["id"], axis=1)

#edges['weight'] = edges['weight']/ edges['weight'].max() 
print(edges['weight'].max())
print(edges.head())
edges.to_csv("dane/edges.csv", index=False)