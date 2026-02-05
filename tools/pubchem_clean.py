import requests

def safe_pubchem_lookup(query: str):
    """
    Only query PubChem if input is a compound-like entity.
    Diseases and genes are ignored safely.
    """
    bad_keywords = [
        "disease", "syndrome", "cancer", "als", "parkinson",
        "alzheimer", "huntington", "diabetes"
    ]

    q = query.lower()
    if any(bad in q for bad in bad_keywords):
        return {"note": "PubChem skipped (non-compound input)"}

    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{query}/property/MolecularWeight,MolecularFormula,IUPACName/JSON"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        props = r.json()["PropertyTable"]["Properties"][0]
        return {
            "compound": query,
            "properties": {
                "molecular_weight": props.get("MolecularWeight"),
                "formula": props.get("MolecularFormula"),
                "iupac_name": props.get("IUPACName")
            },
            "source": "PubChem"
        }
    except Exception:
        return {"note": "PubChem lookup not applicable"}
