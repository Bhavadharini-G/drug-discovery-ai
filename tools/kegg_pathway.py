import requests

def get_pathways_from_kegg(disease_name):
    """
    Query KEGG for pathways associated with a disease name.
    Returns a list of pathway IDs and names.
    """
    # KEGG disease search
    search_url = f"http://rest.kegg.jp/find/disease/{disease_name}"
    resp = requests.get(search_url, timeout=10)
    if resp.status_code != 200:
        return []
    lines = resp.text.strip().split('\n')
    disease_ids = [line.split('\t')[0] for line in lines]
    pathways = []
    for did in disease_ids:
        # Get pathways for each disease
        pw_url = f"http://rest.kegg.jp/link/pathway/{did}"
        pw_resp = requests.get(pw_url, timeout=10)
        if pw_resp.status_code != 200:
            continue
        pw_lines = pw_resp.text.strip().split('\n')
        for pw_line in pw_lines:
            parts = pw_line.split('\t')
            if len(parts) == 2:
                pw_id = parts[1].replace('path:', '')
                pathways.append(pw_id)
    return list(set(pathways))
