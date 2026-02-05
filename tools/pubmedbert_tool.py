import os
import requests

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

MODEL_ID = "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext"
HF_API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

def pubmedbert_summarize(text):
    """
    Uses Hugging Face Inference API (no local torch).
    Predicts masked token completion using PubMedBERT.
    """

    if not HF_API_TOKEN:
        return ["HF_API_TOKEN not set. Cannot run PubMedBERT."]

    prompt = f"{text} is associated with [MASK]."

    payload = {
        "inputs": prompt,
        "parameters": {
            "top_k": 5
        }
    }

    try:
        response = requests.post(
            HF_API_URL,
            headers=HEADERS,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            return [f"HF API error: {response.status_code} - {response.text}"]

        results = response.json()

        formatted = []
        for r in results:
            token = r.get("token_str", "").strip()
            score = r.get("score", 0)
            formatted.append(f"{prompt.replace('[MASK]', token)} (score: {score:.3f})")

        return formatted

    except Exception as e:
        return [f"HF request failed: {str(e)}"]
