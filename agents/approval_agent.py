# agents/approval_agent.py

from tools.regulatory import RegulatoryTool
from tools.pubmedbert_tool import pubmedbert_summarize

class ApprovalAgent:
    def __init__(self):
        self.regulatory = RegulatoryTool()

    def run(self, candidate):
        # SAFETY: candidate may be string
        if isinstance(candidate, str):
            return {
                "approval_report": "Approval analysis requires a compound candidate.",
                "llm_summary": (
                    "Regulatory approval assessment was skipped because "
                    "no compound-level data was provided."
                )
            }

        approval_report = self.regulatory.evaluate(candidate)

        summary_lines = pubmedbert_summarize(
            candidate.get("name", "unknown compound")
        )

        return {
            "approval_report": approval_report,
            "llm_summary": "PubMedBERT summary:\n" + "\n".join(summary_lines)
        }
