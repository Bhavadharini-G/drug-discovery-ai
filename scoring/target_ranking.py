from collections import Counter

def rank_targets(targets):
    counts = Counter(targets)
    total = sum(counts.values())

    ranked = {}
    for gene, freq in counts.items():
        ranked[gene] = round(freq / total, 3)

    return dict(sorted(ranked.items(), key=lambda x: x[1], reverse=True))
