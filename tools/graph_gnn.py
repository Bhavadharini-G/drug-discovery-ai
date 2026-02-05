# tools/graph_gnn.py
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv

class DiseaseGNN(torch.nn.Module):
    def __init__(self, in_dim=16, hidden=32):
        super().__init__()
        self.conv1 = GCNConv(in_dim, hidden)
        self.conv2 = GCNConv(hidden, hidden)
        self.scorer = torch.nn.Linear(hidden, 1)

    def forward(self, data):
        x = F.relu(self.conv1(data.x, data.edge_index))
        x = F.relu(self.conv2(x, data.edge_index))
        scores = self.scorer(x).squeeze(-1)
        return x, scores

def build_graph(nodes, edges):
    if len(nodes) == 0 or len(edges) == 0:
        return None, None

    idx = {n: i for i, n in enumerate(nodes)}
    edge_index = torch.tensor(
        [[idx[a], idx[b]] for a, b in edges],
        dtype=torch.long
    ).t().contiguous()

    x = torch.randn(len(nodes), 16)
    return Data(x=x, edge_index=edge_index), idx

def train_gnn(data, epochs=80):
    model = DiseaseGNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    for _ in range(epochs):
        optimizer.zero_grad()
        _, scores = model(data)
        loss = scores.mean()
        loss.backward()
        optimizer.step()

    return model
