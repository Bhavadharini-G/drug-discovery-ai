import torch
from torch_geometric.data import Data
import networkx as nx


def build_gene_graph(genes):
    """
    Build a simple co-occurrence graph from extracted genes.
    Each gene is a node, edges connect genes appearing together.
    """

    G = nx.Graph()

    # Add nodes
    for gene in genes:
        G.add_node(gene)

    # Co-occurrence edges (fully connected within same document)
    unique_genes = list(set(genes))
    for i in range(len(unique_genes)):
        for j in range(i + 1, len(unique_genes)):
            G.add_edge(unique_genes[i], unique_genes[j])

    # Map genes → indices
    node_map = {gene: i for i, gene in enumerate(G.nodes())}

    edge_index = []
    for u, v in G.edges():
        edge_index.append([node_map[u], node_map[v]])
        edge_index.append([node_map[v], node_map[u]])

    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()

    # Node features: simple identity / frequency placeholder
    x = torch.eye(len(node_map), dtype=torch.float)

    return Data(x=x, edge_index=edge_index), node_map
