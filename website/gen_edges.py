import pandas as pd
import json 
import numpy as np

def load_force_layout(mean_lat, std_lat, mean_lng, std_lng):
    with open("dane/nodes_force_layout.json", "r") as f:
        data = json.load(f)

    data = data['_groups'][0]

    data_procesed = []
    for entry in data:
        data_procesed.append(entry['__data__'])

    dataframe = pd.DataFrame(data_procesed)[['id', 'x', 'y']].rename({'x': 'force_x', 'y': 'force_y'}, axis=1)

    def scale(x, target_mean, target_std):
        src_std = x.std()
        src_mean = x.mean()

        return (x - src_mean) * target_std / src_std + target_mean

    dataframe['force_x'] = scale(dataframe['force_x'], mean_lat, std_lat)
    dataframe['force_y'] = scale(dataframe['force_y'], mean_lng, std_lng)

    dataframe['id'] = dataframe['id'].astype(int)

    return dataframe

nodes = pd.read_csv("dane/stations_names.csv")
calculations = pd.read_csv("dane/node_data.csv")
edges = pd.read_csv("dane/edge_with_weights.csv")

# fix node ordering
calculations['id'] = calculations['id'] - 1

nodes_full = pd.merge(nodes, calculations, left_on='id', right_on='id', how="left")
nodes_force_layout = load_force_layout(
    nodes_full['lat'].mean(),
    nodes_full['lat'].std() * 2,
    nodes_full['lng'].mean(),
    nodes_full['lng'].std() * 2
)

nodes_full = pd.merge(nodes_full, nodes_force_layout, left_on='id', right_on='id', how="left")
nodes_full.to_csv("dane/nodes.csv", index=False)

exit(0)

edges = pd.merge(edges, nodes[["lat", "lng", "id"]], left_on='source', right_on='id', how="left").drop(["id"], axis=1)
edges = pd.merge(edges, nodes[["lat", "lng", "id"]], left_on='target', suffixes=("_source", "_target"), right_on='id', how="left").drop(["id"], axis=1)

# Print edges
#edges['weight'] = edges['weight']/ edges['weight'].max() 
print(edges['weight'].max())
print(edges.head())
edges.to_csv("dane/edges.csv", index=False)