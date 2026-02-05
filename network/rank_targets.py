import torch
from network.graph_builder import build_gene_graph
from network.gnn_model import GeneGCN


def rank_gene_targets(genes, epochs=100):
    """
    Returns ranked gene targets using GNN scores
    """

    data, node_map = build_gene_graph(genes)

    model = GeneGCN(input_dim=data.x.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    # Dummy self-supervised objective
    for _ in range(epochs):
        optimizer.zero_grad()
        out = model(data)
        loss = -out.mean()
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        scores = model(data).cpu().numpy()

    inv_map = {v: k for k, v in node_map.items()}
    ranked = sorted(
        [(inv_map[i], float(scores[i])) for i in range(len(scores))],
        key=lambda x: x[1],
        reverse=True
    )

    return ranked
