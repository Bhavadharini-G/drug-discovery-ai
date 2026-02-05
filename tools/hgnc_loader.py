import pandas as pd
from pathlib import Path

HGNC_PATH = Path("data/hgnc_complete_set.txt")

def load_hgnc_symbols():
    df = pd.read_csv(HGNC_PATH, sep="\t", low_memory=False)
    return set(df["symbol"].dropna().str.upper())
