import networkx as nx

def build_network(disease, gene_counts):
    G = nx.Graph()
    G.add_node(disease, type="disease")

    for gene, freq in gene_counts.items():
        G.add_node(gene, type="gene")
        G.add_edge(disease, gene, weight=freq)

    return G
