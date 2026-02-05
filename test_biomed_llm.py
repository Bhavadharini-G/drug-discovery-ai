# Test script for BioGPT and PubMedBERT
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForMaskedLM, pipeline

print("--- BioGPT Test ---")
biogpt_tokenizer = AutoTokenizer.from_pretrained("microsoft/biogpt")
biogpt_model = AutoModelForCausalLM.from_pretrained("microsoft/biogpt")
# Force CPU usage to avoid MPS (Apple Silicon) incompatibility
biogpt_gen = pipeline("text-generation", model=biogpt_model, tokenizer=biogpt_tokenizer, device=-1)
biogpt_prompt = "Summarize the pharmacological properties of aspirin."
biogpt_result = biogpt_gen(biogpt_prompt, max_new_tokens=100)
print(biogpt_result[0]['generated_text'])

print("\n--- PubMedBERT Test ---")
pubmedbert_tokenizer = AutoTokenizer.from_pretrained("microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract")
pubmedbert_model = AutoModelForMaskedLM.from_pretrained("microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract")
pubmedbert_fill = pipeline("fill-mask", model=pubmedbert_model, tokenizer=pubmedbert_tokenizer)
pubmedbert_result = pubmedbert_fill("Aspirin is used to treat [MASK].")
for r in pubmedbert_result:
    print(f"{r['sequence']} (score: {r['score']:.3f})")
