# tools/pubchem_target.py
# ============================================================
# PUBCHEM COMPOUND LOOKUP (COMPOUND-ONLY, SAFE)
# ============================================================

import requests


def get_compounds_for_target(query, max_results=5):
    """
    PubChem should ONLY be used for compound name lookups.
    This function is intentionally conservative.

    If `query` looks like:
      - aspirin / ibuprofen → works
      - KRAS / APP / BACE1 → safely returns []

    Returns:
        list[dict]: [{ "cid": int, "name": str }]
    """

    # -------------------------------
    # Guard: genes should NOT go here
    # -------------------------------
    if query.isupper() and len(query) <= 10:
        return []

    try:
        # -------------------------------
        # 1️⃣ Resolve compound name → CID
        # -------------------------------
        cid_url = (
            "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
            f"compound/name/{query}/cids/JSON"
        )

        cid_resp = requests.get(cid_url, timeout=10)
        if cid_resp.status_code != 200:
            return []

        cids = cid_resp.json().get("IdentifierList", {}).get("CID", [])
        if not cids:
            return []

        results = []

        # -------------------------------
        # 2️⃣ Fetch IUPAC names
        # -------------------------------
        for cid in cids[:max_results]:
            prop_url = (
                "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
                f"compound/cid/{cid}/property/IUPACName/JSON"
            )

            prop_resp = requests.get(prop_url, timeout=10)
            if prop_resp.status_code == 200:
                props = (
                    prop_resp.json()
                    .get("PropertyTable", {})
                    .get("Properties", [{}])[0]
                )

                results.append({
                    "cid": cid,
                    "name": props.get("IUPACName", "")
                })

        return results

    except Exception:
        return []
