from tools.pubchem_target import get_compounds_for_target

def fetch_gene_compounds(genes, max_results=5):
    gene_to_compounds = {}
    for g in genes:
        compounds = get_compounds_for_target(g, max_results=max_results)
        if isinstance(compounds, list):
            gene_to_compounds[g] = compounds
        else:
            gene_to_compounds[g] = []
    return gene_to_compounds
