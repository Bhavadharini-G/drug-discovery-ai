# tools/target_confidence.py
# ============================================================
# TARGET CONFIDENCE SCORING
# ============================================================

def score_target_confidence(
    pubmed_hits,
    gnn_score=None,
    pathway_hits=0,
    clinical_trials=0
):
    """
    Confidence score ∈ [0,1]
    """

    score = 0.0

    # Literature support
    score += min(len(pubmed_hits) / 10, 0.3)

    # GNN importance
    if gnn_score is not None:
        score += min(abs(gnn_score), 0.3)

    # Pathway evidence
    score += min(pathway_hits * 0.05, 0.2)

    # Clinical validation
    score += min(clinical_trials * 0.1, 0.2)

    return round(min(score, 1.0), 3)
