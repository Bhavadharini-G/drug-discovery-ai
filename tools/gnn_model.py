"""
GNN scoring module.

- Uses full PyTorch + PyG GNN when available (local / research)
- Falls back to heuristic scoring in cloud deployments (Railway-safe)
"""

# -----------------------------
# SAFE TORCH IMPORT
# -----------------------------
try:
    import torch
    import torch.nn.functional as F
    from torch_geometric.data import Data
    from torch_geometric.nn import GCNConv
    TORCH_AVAILABLE = True
except Exception:
    TORCH_AVAILABLE = False


# -----------------------------
# REAL GNN (LOCAL MODE)
# -----------------------------
if TORCH_AVAILABLE:

    class SimpleGNN(torch.nn.Module):
        def __init__(self, dim=16):
            super().__init__()
            self.conv1 = GCNConv(dim, 16)
            self.conv2 = GCNConv(16, 1)

        def forward(self, x, edge_index):
            x = F.relu(self.conv1(x, edge_index))
            return self.conv2(x, edge_index).squeeze()


# -----------------------------
# PUBLIC API (UNCHANGED)
# -----------------------------
def run_gnn(genes, disease):

    if not genes:
        return []

    # ===== CLOUD MODE (NO TORCH) =====
    if not TORCH_AVAILABLE:
        return [
            {"gene": g, "score": round(1.0 / (i + 1), 3)}
            for i, g in enumerate(genes)
        ]

    # ===== LOCAL MODE (FULL GNN) =====
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
    model.eval()

    with torch.no_grad():
        out = model(data.x, data.edge_index)

    return sorted(
        [{"gene": genes[i], "score": float(out[i])} for i in range(len(genes))],
        key=lambda x: x["score"],
        reverse=True
    )
