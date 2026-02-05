def normalize(value, min_v, max_v):
    if value is None:
        return 0.0
    return max(0.0, min(1.0, (value - min_v) / (max_v - min_v)))


def score_compound(
    docking_score=None,
    ic50=None,
    qed=None,
    admet=None
):
    docking = normalize(-docking_score, 0, 15) if docking_score else 0.0
    bioactivity = normalize(ic50, 0, 10000) if ic50 else 0.0
    drug_like = qed if qed else 0.0
    admet_score = admet if admet else 0.0

    final_score = (
        0.35 * docking +
        0.25 * bioactivity +
        0.20 * drug_like +
        0.20 * admet_score
    )

    return round(final_score, 3)
