# tools/network.py

import networkx as nx

# Example: Build a disease network from pathways and targets
def build_disease_network(pathways, targets):
    G = nx.Graph()
    for pathway in pathways:
        G.add_node(pathway, type='pathway')
    for target in targets:
        G.add_node(target, type='gene')
        for pathway in pathways:
            G.add_edge(pathway, target)
    return G

# Example: Run a simple GNN/digital-twin analysis (placeholder)
def run_gnn_analysis(network):
    # Placeholder: assign random scores to each target
    import random
    insights = {n: random.random() for n, d in network.nodes(data=True) if d['type'] == 'gene'}
    return insights
