# ============================================================
# HGNC-AWARE, VERSION-PROOF GENE EXTRACTION MODULE
# ============================================================

import os
import re
from typing import List, Set

# ------------------------------------------------------------
# 1. Locate HGNC file
# ------------------------------------------------------------

def find_hgnc_file() -> str:
    base = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base, "data")

    for f in os.listdir(data_dir):
        if "hgnc" in f.lower() and f.lower().endswith(".txt"):
            return os.path.join(data_dir, f)

    raise FileNotFoundError("❌ No HGNC .txt file found in data/")

# ------------------------------------------------------------
# 2. Load HGNC gene symbols (AUTO COLUMN DETECTION)
# ------------------------------------------------------------

def load_hgnc_genes() -> Set[str]:
    path = find_hgnc_file()
    genes = set()

    with open(path, encoding="utf-8", errors="ignore") as f:
        header = f.readline().strip().lower().split("\t")

        symbol_candidates = {
            "approved symbol",
            "symbol",
            "gene symbol",
            "approved_symbol",
            "hgnc symbol",
        }

        symbol_idx = None
        for i, col in enumerate(header):
            if col.strip() in symbol_candidates:
                symbol_idx = i
                break

        if symbol_idx is None:
            raise RuntimeError(
                f"❌ HGNC symbol column not found.\n"
                f"Found columns: {header[:10]}"
            )

        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) <= symbol_idx:
                continue

            gene = parts[symbol_idx].upper().strip()

            if (
                2 <= len(gene) <= 10
                and gene[0].isalpha()
                and gene.isalnum()
            ):
                genes.add(gene)

    if not genes:
        raise RuntimeError("❌ HGNC parsed but ZERO genes extracted.")

    print(f"✅ HGNC loaded successfully: {len(genes)} genes")
    return genes


HGNC_GENES = load_hgnc_genes()

# ------------------------------------------------------------
# 3. STOPWORDS (NEVER genes)
# ------------------------------------------------------------

STOPWORDS = {
    # Grammar
    "AND", "OR", "IN", "ON", "WITH", "BY", "FROM",

    # Biomedical terms
    "PCR", "ELISA", "MRI", "CT", "MS", "MSN",
    "MICE", "HUMAN", "PATIENT", "PATIENTS",
    "IMPACT", "COPE", "PC", "SI", "STS", "KIN",
    "GPT", "CARE", "MEAN", "SEX", "NE",

    # Disease words
    "DISEASE", "DISORDER", "SYNDROME",
    "CAUSE", "CAUSES", "MUTATION",

    # Units / stats
    "SD", "SE", "CI", "HR", "OR",
}

# Short valid genes (explicit whitelist)
SHORT_GENE_WHITELIST = {
    "HTT", "APP", "MAPT", "PSEN1", "PSEN2"
}

# ------------------------------------------------------------
# 4. Gene regex (HGNC-like)
# ------------------------------------------------------------

GENE_REGEX = re.compile(r"\b[A-Z][A-Z0-9]{1,9}\b")

# ------------------------------------------------------------
# 5. Optional Biomedical NER (SAFE)
# ------------------------------------------------------------

NER_PIPELINE = None

def load_ner():
    global NER_PIPELINE
    if NER_PIPELINE:
        return NER_PIPELINE

    try:
        from transformers import pipeline
        NER_PIPELINE = pipeline(
            "ner",
            model="d4data/biomedical-ner-all",
            aggregation_strategy="simple"
        )
    except Exception:
        NER_PIPELINE = None

    return NER_PIPELINE

# ------------------------------------------------------------
# 6. OPTIONAL FALLBACK (BIOLOGICALLY VERIFIED)
# ------------------------------------------------------------

KNOWN_DISEASE_GENES = {
    "huntington's disease": ["HTT"],
    "alzheimer's disease": ["APP", "PSEN1", "PSEN2", "BACE1"],
    "parkinson's disease": ["SNCA", "LRRK2"],
    "glioblastoma": ["EGFR", "PTEN", "TP53"],
    "breast cancer": ["BRCA1", "BRCA2", "TP53"]
}

# ------------------------------------------------------------
# 7. FINAL GENE EXTRACTION (HGNC = AUTHORITY)
# ------------------------------------------------------------

def extract_genes(texts: List[str], disease: str = None) -> List[str]:
    found = set()
    ner = load_ner()

    for text in texts:
        text_u = text.upper()

        # -------- RULE-BASED PASS --------
        for token in GENE_REGEX.findall(text_u):

            if len(token) < 4 and token not in SHORT_GENE_WHITELIST:
                continue

            if token in STOPWORDS:
                continue

            if token not in HGNC_GENES:
                continue

            found.add(token)

        # -------- NER ASSIST (STRICT FILTER) --------
        if ner:
            try:
                for ent in ner(text):
                    word = ent.get("word", "").replace("##", "").upper()

                    if (
                        word in HGNC_GENES
                        and word not in STOPWORDS
                        and (len(word) >= 4 or word in SHORT_GENE_WHITELIST)
                    ):
                        found.add(word)
            except Exception:
                pass

    # -------- SAFE FALLBACK (OPTIONAL) --------
    if not found and disease:
        found.update(KNOWN_DISEASE_GENES.get(disease.lower(), []))

    return sorted(found)
