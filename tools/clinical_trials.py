# ============================================================
# CLINICAL TRIALS MODULE
# ============================================================

import os
import pandas as pd

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

CSV_PATH = os.path.join("data", "clinical_trials.csv")


# ------------------------------------------------------------
# LOAD CSV SAFELY
# ------------------------------------------------------------

def load_clinical_trials():
    """
    Load clinical trials CSV safely.
    """
    if not os.path.exists(CSV_PATH):
        print("⚠️ clinical_trials.csv not found")
        return pd.DataFrame()

    try:
        return pd.read_csv(CSV_PATH)
    except Exception as e:
        print("❌ Failed to load clinical trials:", e)
        return pd.DataFrame()


# ------------------------------------------------------------
# QUERY TRIALS (USED BY FASTAPI & DISCOVERY AGENT)
# ------------------------------------------------------------

def get_trials_for_query(query: str):
    """
    Find clinical trials related to a disease / gene / compound.

    Returns:
        list[dict]
    """
    df = load_clinical_trials()
    if df.empty:
        return []

    q = query.lower()

    hits = df[
        df.apply(
            lambda row: any(
                q in str(row[col]).lower()
                for col in ["condition", "intervention", "target", "gene"]
                if col in df.columns
            ),
            axis=1
        )
    ]

    return hits.to_dict(orient="records")


# ------------------------------------------------------------
# CLINICAL CONFIDENCE SCORE (OPTIONAL, USED BY DISCOVERY)
# ------------------------------------------------------------

def clinical_confidence(trials):
    """
    Score clinical evidence strength.

    Phase 3 → +3
    Phase 2 → +2
    Phase 1 → +1
    """
    score = 0

    for t in trials:
        phase = str(t.get("phase", "")).lower()

        if "phase 3" in phase:
            score += 3
        elif "phase 2" in phase:
            score += 2
        elif "phase 1" in phase:
            score += 1

    return score
