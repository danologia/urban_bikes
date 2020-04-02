import pandas as pd
import json

def load_force_layout():
    with open("dane/nodes_fg.json", "r") as f:
        data = json.load(f)

    data = data['_groups'][0]

    data_procesed = []
    for entry in data:
        data_procesed.append(entry['__data__'])

    dataframe = pd.DataFrame(data_procesed)[['id', 'x', 'y']]

    return dataframe
