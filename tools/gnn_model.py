import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv

class SimpleGNN(torch.nn.Module):
    def __init__(self, dim=16):
        super().__init__()
        self.conv1 = GCNConv(dim, 16)
        self.conv2 = GCNConv(16, 1)

    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        return self.conv2(x, edge_index).squeeze()

def run_gnn(genes, disease):
    if not genes:
        return []

    # simple chain graph
    edges = []
    for i in range(len(genes) - 1):
        edges.append((i, i + 1))
        edges.append((i + 1, i))

    if not edges:
        return [{"gene": genes[0], "score": 1.0}]

    edge_index = torch.tensor(edges).t().contiguous()
    x = torch.randn(len(genes), 16)

    data = Data(x=x, edge_index=edge_index)
    model = SimpleGNN()
    out = model(data.x, data.edge_index)

    return sorted(
        [{"gene": genes[i], "score": float(out[i])} for i in range(len(genes))],
        key=lambda x: x["score"],
        reverse=True
    )
