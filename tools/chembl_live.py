import requests

def get_compounds_for_target(target, limit=5):
    url = f"https://www.ebi.ac.uk/chembl/api/data/target/search?q={target}"
    r = requests.get(url).json()

    compounds = []
    for t in r.get("targets", [])[:1]:
        tid = t["target_chembl_id"]
        act_url = f"https://www.ebi.ac.uk/chembl/api/data/activity?target_chembl_id={tid}&limit={limit}"
        acts = requests.get(act_url).json()

        for a in acts.get("activities", []):
            if a.get("molecule_chembl_id"):
                compounds.append(a["molecule_chembl_id"])

    return list(set(compounds))
