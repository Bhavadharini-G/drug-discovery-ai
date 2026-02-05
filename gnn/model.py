import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class DiseaseGNN(torch.nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.conv1 = GCNConv(dim, 32)
        self.conv2 = GCNConv(32, 1)

    def forward(self, data):
        h = F.relu(self.conv1(data.x, data.edge_index))
        scores = self.conv2(h).squeeze()
        return h, scores
