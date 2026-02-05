from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline

def biobert_summarize(text):
    """
    Use BioBERT (or PubMedBERT) to extract biomedical knowledge or summarize a protein/gene target.
    """
    tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
    model = AutoModelForMaskedLM.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
    fill_mask = pipeline("fill-mask", model=model, tokenizer=tokenizer)
    # Example: fill a masked sentence about the target
    prompt = f"{text} is involved in [MASK]."
    results = fill_mask(prompt)
    return [f"{r['sequence']} (score: {r['score']:.3f})" for r in results]
