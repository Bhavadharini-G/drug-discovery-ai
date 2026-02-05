import os

def load_hgnc_genes():
    base = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base, "data", "hgnc_complete_set.txt")

    genes = set()
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            g = line.strip().upper()
            if g:
                genes.add(g)
    return genes
