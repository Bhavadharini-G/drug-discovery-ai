import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

MODEL_NAME = "dmis-lab/biobert-v1.1"

@torch.no_grad()
def extract_genes_from_abstracts(abstracts, hgnc_set=None):
    """
    Run BioBERT NER on PubMed abstracts.
    Returns a ranked dict of HGNC gene symbols.
    """

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME)

    nlp = pipeline(
        "ner",
        model=model,
        tokenizer=tokenizer,
        aggregation_strategy="simple"
    )

    gene_counts = {}

    for text in abstracts:
        if not text or len(text) < 20:
            continue

        entities = nlp(text)

        for ent in entities:
            label = ent.get("entity_group", "")
            word = ent.get("word", "").upper()

            # BioBERT uses GENE/PROTEIN labels
            if label in ["GENE", "PROTEIN"]:
                if hgnc_set is None or word in hgnc_set:
                    gene_counts[word] = gene_counts.get(word, 0) + 1

    # Sort by frequency
    ranked = dict(sorted(gene_counts.items(), key=lambda x: x[1], reverse=True))
    return ranked
