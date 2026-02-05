# ============================================================
# AUTO DOCK VINA RUNNER (REAL DOCKING ENGINE)
# ============================================================

import os
import subprocess


# ============================================================
# PATH CONFIGURATION
# ============================================================

# Expected directory structure
BASE_DIR = os.getcwd()

ALPHAFOLD_DIR = os.path.join(BASE_DIR, "data", "alphafold_structures")
LIGAND_DIR = os.path.join(BASE_DIR, "data", "ligands")

# Vina executable (works in WSL OR Windows PATH)
VINA_CMD = "vina"


# ============================================================
# SAFETY CHECKS
# ============================================================

def _exists(path):
    return path and os.path.exists(path)


# ============================================================
# DOCKING FUNCTION
# ============================================================

def run_docking_vina(gene: str, ligand_name: str):
    """
    Runs AutoDock Vina docking and returns binding affinity (kcal/mol)

    Returns:
        float | None
    """

    receptor_pdb = os.path.join(ALPHAFOLD_DIR, f"{gene}.pdb")
    ligand_pdbqt = os.path.join(LIGAND_DIR, f"{ligand_name}.pdbqt")

    # ---------- SAFETY ----------
    if not _exists(receptor_pdb):
        print(f"⚠️ Receptor missing: {receptor_pdb}")
        return None

    if not _exists(ligand_pdbqt):
        print(f"⚠️ Ligand missing: {ligand_pdbqt}")
        return None

    # ---------- VINA COMMAND ----------
    cmd = [
        VINA_CMD,
        "--receptor", receptor_pdb,
        "--ligand", ligand_pdbqt,
        "--center_x", "0",
        "--center_y", "0",
        "--center_z", "0",
        "--size_x", "25",
        "--size_y", "25",
        "--size_z", "25"
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        output = result.stdout + result.stderr

        # ---------- PARSE SCORE ----------
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("1 "):  # first docking pose
                return float(line.split()[1])

    except Exception as e:
        print("❌ Docking error:", e)

    return None
