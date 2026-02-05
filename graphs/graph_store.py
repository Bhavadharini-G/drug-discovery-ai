import networkx as nx
import json

def save_graph(G, path="graphs/disease_graph.json"):
    data = nx.node_link_data(G)
    with open(path, "w") as f:
        json.dump(data, f)

def load_graph(path="graphs/disease_graph.json"):
    with open(path) as f:
        data = json.load(f)
    return nx.node_link_graph(data)
