
# agents/validation_agent.py
"""
ValidationAgent enhancements:
1. Integrates real Lab and Clinical tools.
2. Adds LLM summarization using local Ollama (configurable model).
3. Formats prompt for readability and context.
4. Accumulates full streamed LLM output.
5. Model is configurable via constructor.
6. Modular and ready for extension.
"""

from tools.lab import LabTool
from tools.clinical import ClinicalTool
from tools.pubmedbert_tool import pubmedbert_summarize


class ValidationAgent:
    def __init__(self):
        self.lab = LabTool()
        self.clinical = ClinicalTool()

    def run(self, candidate):
        lab_result = self.lab.test(candidate)
        clinical_result = self.clinical.trial(candidate)
        # Use PubMedBERT for summarization
        pubmedbert_summary = pubmedbert_summarize(candidate)
        llm_summary = "PubMedBERT summary (top predictions):\n" + "\n".join(pubmedbert_summary)
        return {
            "lab_result": lab_result,
            "clinical_result": clinical_result,
            "llm_summary": llm_summary
        }
