import requests

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

def fetch_clinical_trials(disease, limit=20):
    params = {
        "query.term": disease,
        "pageSize": limit
    }
    r = requests.get(BASE_URL, params=params, timeout=10)
    r.raise_for_status()

    trials = []
    for study in r.json().get("studies", []):
        protocol = study.get("protocolSection", {})
        idmod = protocol.get("identificationModule", {})
        status = protocol.get("statusModule", {})
        trials.append({
            "nct_id": idmod.get("nctId"),
            "title": idmod.get("briefTitle"),
            "status": status.get("overallStatus")
        })
    return trials
