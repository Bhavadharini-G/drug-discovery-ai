# tools/pubchem.py

import requests
import re


class PubChemTool:
    """
    Safe PubChem lookup utility.

    ✔ Skips diseases / genes automatically
    ✔ Never throws exceptions to callers
    ✔ Always returns UI-safe JSON
    """

    # Keywords that clearly indicate NON-compounds
    NON_COMPOUND_KEYWORDS = {
        "disease", "syndrome", "cancer", "als", "parkinson",
        "alzheimer", "huntington", "diabetes", "covid",
        "gene", "protein", "mutation"
    }

    GENE_LIKE_REGEX = re.compile(r"^[A-Z0-9]{2,10}$")

    def lookup(self, compound):
        """
        Lookup compound info from PubChem.

        Returns:
            dict with stable keys:
            - is_compound: bool
            - compound / info
        """

        if not compound or not isinstance(compound, str):
            return {
                "is_compound": False,
                "info": "Invalid compound input."
            }

        name = compound.strip()

        # ---------- HARD FILTER: NON-COMPOUNDS ----------
        lower = name.lower()

        if any(word in lower for word in self.NON_COMPOUND_KEYWORDS):
            return {
                "is_compound": False,
                "info": "PubChem lookup skipped (not a compound)."
            }

        # Gene-like symbols (APP, TP53, KRAS)
        if self.GENE_LIKE_REGEX.match(name.upper()):
            return {
                "is_compound": False,
                "info": "PubChem lookup skipped (gene/protein input)."
            }

        # ---------- BUILD PUBCHEM URL ----------
        if name.isdigit():
            url = (
                "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
                f"compound/cid/{name}/property/"
                "MolecularWeight,MolecularFormula,IUPACName/JSON"
            )
        else:
            url = (
                "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
                f"compound/name/{name}/property/"
                "MolecularWeight,MolecularFormula,IUPACName/JSON"
            )

        # ---------- QUERY PUBCHEM ----------
        try:
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                return {
                    "is_compound": False,
                    "info": "Compound not found in PubChem."
                }

            data = r.json()
            props = data.get("PropertyTable", {}).get("Properties", [])

            if not props:
                return {
                    "is_compound": False,
                    "info": "Compound not found in PubChem."
                }

            p = props[0]

            return {
                "is_compound": True,
                "compound": name,
                "molecular_weight": p.get("MolecularWeight"),
                "formula": p.get("MolecularFormula"),
                "iupac_name": p.get("IUPACName"),
                "source": "PubChem"
            }

        except Exception:
            return {
                "is_compound": False,
                "info": "Compound not found in PubChem."
            }
