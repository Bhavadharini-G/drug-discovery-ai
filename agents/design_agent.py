"""
DesignAgent enhancements:
1. Integrates real PubChem, Docking, and QSAR tools.
2. Adds PubMedBERT summarization.
3. Skips invalid PubChem lookups (diseases / targets).
4. Supports single-compound and multi-compound workflows.
5. Modular and ready for extension.
"""

from tools.pubchem import PubChemTool
from tools.docking import DockingTool
from tools.qsar import QSARTool
from tools.pubmedbert_tool import pubmedbert_summarize


class DesignAgent:
    def __init__(self):
        self.pubchem = PubChemTool()
        self.docking = DockingTool()
        self.qsar = QSARTool()

    def _is_valid_compound(self, name: str) -> bool:
        """
        PubChem works ONLY for real chemical compounds.
        """
        if not name:
            return False
        name = name.lower()
        invalid_terms = [
            "disease", "syndrome", "cancer",
            "als", "parkinson", "alzheimer",
            "protein", "gene"
        ]
        return not any(t in name for t in invalid_terms)

    def run(self, compound, compounds_for_target=None):
        """
        Design stage:
        - If compounds_for_target is provided → analyze all
        - Else → analyze single compound
        """

        # ============================
        # MULTI-COMPOUND MODE
        # ============================
        if compounds_for_target and isinstance(compounds_for_target, list):
            analyzed = []

            for c in compounds_for_target:
                cid = c.get("cid")
                name = c.get("iupac_name") or str(cid)

                # PubChem (clean)
                compound_info = (
                    self.pubchem.lookup(name)
                    if self._is_valid_compound(name)
                    else {"info": "PubChem lookup skipped (not a compound)."}
                )

                docking_result = self.docking.screen(name)
                qsar_result = self.qsar.predict(name)

                pubmedbert_summary = pubmedbert_summarize(name)
                llm_summary = (
                    "PubMedBERT summary (top predictions):\n"
                    + "\n".join(pubmedbert_summary)
                )

                analyzed.append({
                    "compound": name,
                    "cid": cid,
                    "compound_info": compound_info,
                    "docking_result": docking_result,
                    "qsar_result": qsar_result,
                    "llm_summary": llm_summary
                })

            return {"analyzed_compounds": analyzed}

        # ============================
        # SINGLE-COMPOUND MODE
        # ============================
        compound_info = (
            self.pubchem.lookup(compound)
            if self._is_valid_compound(compound)
            else {"info": "PubChem lookup skipped (not a compound)."}
        )

        docking_result = self.docking.screen(compound)
        qsar_result = self.qsar.predict(compound)

        pubmedbert_summary = pubmedbert_summarize(compound)
        llm_summary = (
            "PubMedBERT summary (top predictions):\n"
            + "\n".join(pubmedbert_summary)
        )

        return {
            "compound_info": compound_info,
            "docking_result": docking_result,
            "qsar_result": qsar_result,
            "llm_summary": llm_summary
        }
