
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline

# Global cache for model, tokenizer, and pipeline
_pubmedbert_tokenizer = None
_pubmedbert_model = None
_pubmedbert_fill_mask = None

def get_pubmedbert_pipeline():
    global _pubmedbert_tokenizer, _pubmedbert_model, _pubmedbert_fill_mask
    if _pubmedbert_tokenizer is None or _pubmedbert_model is None or _pubmedbert_fill_mask is None:
        _pubmedbert_tokenizer = AutoTokenizer.from_pretrained("microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext")
        _pubmedbert_model = AutoModelForMaskedLM.from_pretrained("microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext")
        _pubmedbert_fill_mask = pipeline("fill-mask", model=_pubmedbert_model, tokenizer=_pubmedbert_tokenizer)
    return _pubmedbert_fill_mask

def pubmedbert_summarize(text):
    """
    Use PubMedBERT to extract biomedical knowledge or summarize a protein/gene/compound.
    Caches model and tokenizer for fast repeated calls.
    """
    fill_mask = get_pubmedbert_pipeline()
    prompt = f"{text} is associated with [MASK]."
    results = fill_mask(prompt)
    return [f"{r['sequence']} (score: {r['score']:.3f})" for r in results]
