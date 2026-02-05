import pandas as pd
import os

# Paths
INPUT_FILE = "data/hgnc_complete_set.txt"
OUTPUT_FILE = "tools/hgnc_symbols.txt"

# Ensure tools directory exists
os.makedirs("tools", exist_ok=True)

# Load HGNC TSV safely
df = pd.read_csv(
    INPUT_FILE,
    sep="\t",
    encoding="utf-8",
    low_memory=False
)

# Extract gene symbols
symbols = (
    df["symbol"]
    .dropna()
    .astype(str)
    .str.upper()
    .unique()
)

# Write one gene per line
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for gene in symbols:
        f.write(gene + "\n")

print(f"✅ Generated {len(symbols)} gene symbols → {OUTPUT_FILE}")
