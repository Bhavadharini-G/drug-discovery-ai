# tools/pubmed.py
# ============================================================
# PUBMED SEARCH TOOL (CLEAN, SAFE, HGNC-COMPATIBLE)
# ============================================================

import requests


class PubMedTool:
    """
    PubMed search utility.

    ✔ Returns ONLY PubMed IDs (PMIDs)
    ✔ Never returns text errors
    ✔ Safe for gene extraction
    ✔ NCBI-compliant
    """

    def __init__(self, email="researcher@example.com", tool="drug-discovery-ai"):
        self.email = email
        self.tool = tool

    def search(self, query: str, retmax: int = 5):
        """
        Search PubMed and return a list of PMIDs.

        Args:
            query (str): Disease, gene, or compound
            retmax (int): Number of PMIDs

        Returns:
            list[str]: PubMed IDs
        """

        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": retmax,
            "tool": self.tool,
            "email": self.email
        }

        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            return data.get("esearchresult", {}).get("idlist", [])

        except Exception:
            # Silent fail — NEVER return text
            return []
