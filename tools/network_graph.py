import networkx as nx

def build_disease_network(disease, genes, compounds=None):
    """
    Build disease-gene-compound graph
    """
    G = nx.Graph()

    # Add disease node
    G.add_node(disease, type="disease")

    # Add gene nodes
    for g in genes:
        G.add_node(g, type="gene")
        G.add_edge(disease, g)

    # Add compound nodes (optional)
    if compounds:
        for gene, clist in compounds.items():
            for c in clist:
                cname = c.get("iupac_name") or str(c.get("cid"))
                G.add_node(cname, type="compound")
                G.add_edge(gene, cname)

    return G


def rank_targets(G):
    """
    Rank genes using graph centrality (GNN proxy)
    """
    centrality = nx.degree_centrality(G)

    gene_scores = {
        n: score
        for n, score in centrality.items()
        if G.nodes[n].get("type") == "gene"
    }

    return dict(sorted(gene_scores.items(), key=lambda x: x[1], reverse=True))
