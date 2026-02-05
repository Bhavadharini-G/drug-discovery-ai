import os
import requests

ALPHAFOLD_BASE_URL = "https://alphafold.ebi.ac.uk/files/"

# Example: {'BACE1': 'P56817', 'APP': 'P05067', ...}
ALZHEIMER_PROTEINS = {
    'BACE1': 'P56817',
    'APP': 'P05067',
    'PSEN1': 'P49768',
    'PSEN2': 'P49810',
    'MAPT': 'P10636',
    'APOE': 'P02649',
}

def download_alphafold_structures(protein_dict, out_dir="data/alphafold_structures"):
    os.makedirs(out_dir, exist_ok=True)
    for name, uniprot_id in protein_dict.items():
        pdb_filename = f"AF-{uniprot_id}-F1-model_v4.pdb"
        url = ALPHAFOLD_BASE_URL + pdb_filename
        out_path_uniprot = os.path.join(out_dir, f"{uniprot_id}.pdb")
        out_path_name = os.path.join(out_dir, f"{name}.pdb")
        # Download if either file is missing
        if os.path.exists(out_path_uniprot) and os.path.exists(out_path_name):
            print(f"[SKIP] {out_path_uniprot} and {out_path_name} already exist.")
            continue
        print(f"[DOWNLOAD] {url} -> {out_path_uniprot} and {out_path_name}")
        try:
            resp = requests.get(url, timeout=20)
            if resp.status_code == 200:
                with open(out_path_uniprot, "wb") as f:
                    f.write(resp.content)
                with open(out_path_name, "wb") as f:
                    f.write(resp.content)
                print(f"[OK] Downloaded {out_path_uniprot} and {out_path_name}")
            else:
                print(f"[ERROR] Failed to download {url} (status {resp.status_code})")
        except Exception as e:
            print(f"[ERROR] Exception downloading {url}: {e}")

if __name__ == "__main__":
    download_alphafold_structures(ALZHEIMER_PROTEINS)
