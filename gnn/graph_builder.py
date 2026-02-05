import torch
from torch_geometric.data import Data

def build_graph(disease, genes, compounds):
    nodes = [disease] + genes + compounds
    idx = {n: i for i, n in enumerate(nodes)}
    edges = []

    for g in genes:
        edges += [[idx[disease], idx[g]], [idx[g], idx[disease]]]

    for g in genes:
        for c in compounds:
            edges += [[idx[g], idx[c]], [idx[c], idx[g]]]

    if not edges:
        edges = [[0, 0]]

    edge_index = torch.tensor(edges).t().contiguous()
    x = torch.eye(len(nodes))

    return Data(x=x, edge_index=edge_index), nodes
