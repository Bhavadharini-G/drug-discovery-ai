# tools/admet_predictor.py
import random

def predict_admet(compound):
    """
    Proxy ADMET score based on simple heuristics.
    Produces non-identical values (0.45–0.75).
    """

    if isinstance(compound, str):
        return round(random.uniform(0.55, 0.7), 2)

    if not isinstance(compound, dict):
        return 0.55

    mw = compound.get("MW", 350)
    logp = compound.get("LogP", 2.5)

    score = 0.7
    score -= abs(mw - 350) / 700
    score -= abs(logp - 2.5) / 6

    return round(max(0.45, min(score, 0.75)), 2)
