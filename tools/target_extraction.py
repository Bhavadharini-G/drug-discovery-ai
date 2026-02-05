import requests
from collections import Counter
import re

# Helper to fetch PubMed abstracts for a list of PMIDs

def fetch_pubmed_abstracts(pmids, retmax=3):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "text",
        "rettype": "abstract"
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return ""

# Simple protein/gene name extraction (NER can be added later)

# Regex-based fallback extraction
def extract_targets_from_abstracts(abstracts, top_n=5):
    matches = re.findall(r'\b[A-Z0-9]{2,10}\b', abstracts)
    blacklist = set(["AND", "THE", "FOR", "WITH", "FROM", "THIS", "THAT", "WAS", "ARE", "HAVE", "HAS", "WERE", "NOT", "BUT", "ALL", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN"])
    filtered = [m for m in matches if not m.isdigit() and m not in blacklist and len(m) > 2]
    counter = Counter(filtered)
    return [name for name, _ in counter.most_common(top_n)]

# BioBERT-based NER extraction
def extract_targets_biobert(abstracts, top_n=5):
    """
    Extracts biomedical entities (genes/proteins/diseases) from abstracts using BioBERT NER.
    Requires: pip install transformers torch
    """
    try:
        from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
    except ImportError:
        raise ImportError("transformers and torch must be installed to use BioBERT NER.")

    model_name = "d4data/biobert-ner"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

    # If abstracts is a list, join to a single string
    if isinstance(abstracts, list):
        text = "\n".join(abstracts)
    else:
        text = abstracts

    results = nlp(text)
    # Filter for gene/protein/disease entities (BioBERT NER tags: GENE, DISEASE, etc.)
    entities = [ent['word'] for ent in results if ent['entity_group'] in {"GENE", "PROTEIN", "DISEASE"}]
    counter = Counter(entities)
    return [name for name, _ in counter.most_common(top_n)]
