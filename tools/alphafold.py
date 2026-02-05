# ============================================================
# SAFE ALPHAFOLD TOOL
# ============================================================

import requests

class AlphaFoldTool:

    def predict(self, gene: str):
        try:
            url = f"https://alphafold.ebi.ac.uk/api/prediction/{gene}"
            r = requests.get(url, timeout=5)

            if r.status_code != 200:
                raise Exception("AlphaFold not available")

            return {
                "found": True,
                "manual_link": f"https://alphafold.ebi.ac.uk/search/text/{gene}"
            }

        except Exception:
            return {
                "found": False,
                "manual_link": f"https://alphafold.ebi.ac.uk/search/text/{gene}",
                "message": "AlphaFold unavailable (timeout-safe fallback)."
            }
