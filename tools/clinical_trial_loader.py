import pandas as pd
import os

CSV_PATH = os.path.join("data", "clinical_trials.csv")

def load_clinical_trials():
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()

    return pd.read_csv(CSV_PATH)


def get_trials_for_query(query: str):
    df = load_clinical_trials()
    if df.empty:
        return []

    q = query.lower()

    hits = df[
        df.apply(
            lambda row: any(
                q in str(row[col]).lower()
                for col in ["condition", "intervention", "target"]
                if col in df.columns
            ),
            axis=1
        )
    ]

    return hits.to_dict(orient="records")
