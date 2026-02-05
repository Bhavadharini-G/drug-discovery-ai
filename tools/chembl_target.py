# tools/chembl_target.py
# ============================================================
# REAL ChEMBL TARGET → COMPOUND LOADER (TIMEOUT-SAFE)
# ============================================================

import requests

BASE = "https://www.ebi.ac.uk/chembl/api/data"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "DrugDiscoveryAI/1.0"
}

TIMEOUT = 20   # 🔧 increased timeout


# ------------------------------------------------------------
# STEP 1: Resolve gene → ChEMBL target ID (SAFE)
# ------------------------------------------------------------
def get_target_chembl_id(gene: str):
    url = f"{BASE}/target/search.json?q={gene}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
    except Exception:
        # 🚫 Network failure / timeout → safe fallback
        return None

    data = r.json().get("targets", [])

    for t in data:
        if t.get("target_type") == "SINGLE PROTEIN":
            return t.get("target_chembl_id")

    return None


# ------------------------------------------------------------
# STEP 2: Fetch activities + molecule info (SAFE)
# ------------------------------------------------------------
def get_chembl_compounds_for_target(gene: str, limit=5):
    """
    Always returns a list.
    NEVER raises network exceptions.
    """

    target_id = get_target_chembl_id(gene)
    if not target_id:
        return []

    url = f"{BASE}/activity.json"
    params = {
        "target_chembl_id": target_id,
        "standard_type__in": "IC50,EC50,Ki",
        "limit": 50
    }

    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
    except Exception:
        # 🚫 EBI timeout / rate-limit → safe fallback
        return []

    activities = r.json().get("activities", [])
    compounds = []

    for act in activities:
        # HARD FILTER — must have activity
        if not act.get("standard_value") or not act.get("standard_units"):
            continue

        mol_id = act.get("molecule_chembl_id")
        if not mol_id:
            continue

        try:
            value = float(act.get("standard_value"))
        except Exception:
            continue

        compounds.append({
            "name": mol_id,
            "activity_type": act.get("standard_type"),
            "activity_value": value,
            "activity_units": act.get("standard_units"),
            "bioactivity_score": act.get("pchembl_value") or 0.5,
        })

        if len(compounds) >= limit:
            break

    return compounds
