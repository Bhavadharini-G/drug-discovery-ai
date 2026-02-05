# ============================================================
# RECEPTOR PREPARATION (PDB → PDBQT)
# ============================================================

import os
import shutil
import subprocess


# ============================================================
# PATH CONFIGURATION (PROJECT-SAFE)
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ALPHAFOLD_DIR = os.path.join(BASE_DIR, "data", "alphafold_structures")
RECEPTOR_DIR = os.path.join(BASE_DIR, "data", "receptors")

os.makedirs(RECEPTOR_DIR, exist_ok=True)


# ============================================================
# FIND AutoDockTools SCRIPT
# ============================================================

def find_prepare_receptor():
    """
    Locate prepare_receptor4.py safely.
    """
    candidates = [
        "prepare_receptor4.py",
        shutil.which("prepare_receptor4.py"),
        shutil.which("prepare_receptor"),
    ]

    for c in candidates:
        if c and os.path.exists(c):
            return c

    raise RuntimeError(
        "❌ prepare_receptor4.py not found.\n"
        "Install AutoDockTools and ensure it is on PATH."
    )


PREPARE_RECEPTOR = find_prepare_receptor()


# ============================================================
# CORE FUNCTION
# ============================================================

def prepare_receptor(gene: str, force: bool = False):
    """
    Prepare protein receptor for docking

    Args:
        gene (str): gene/protein name (HGNC)
        force (bool): overwrite existing PDBQT

    Returns:
        dict:
        {
          "status": "ok" | "error",
          "path": str | None,
          "message": str
        }
    """

    gene = gene.strip().upper()

    pdb_file = os.path.join(ALPHAFOLD_DIR, f"{gene}.pdb")
    pdbqt_file = os.path.join(RECEPTOR_DIR, f"{gene}.pdbqt")

    if not os.path.exists(pdb_file):
        return {
            "status": "error",
            "path": None,
            "message": f"Missing AlphaFold PDB for {gene}"
        }

    if os.path.exists(pdbqt_file) and not force:
        return {
            "status": "ok",
            "path": pdbqt_file,
            "message": "Receptor already prepared"
        }

    try:
        cmd = [
            PREPARE_RECEPTOR,
            "-r", pdb_file,
            "-o", pdbqt_file,
            "-A", "hydrogens"
        ]

        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=True
        )

        if os.path.exists(pdbqt_file):
            return {
                "status": "ok",
                "path": pdbqt_file,
                "message": "Receptor prepared successfully"
            }

    except Exception as e:
        return {
            "status": "error",
            "path": None,
            "message": f"prepare_receptor4.py failed: {e}"
        }

    return {
        "status": "error",
        "path": None,
        "message": "Unknown receptor preparation error"
    }


# ============================================================
# 🔗 NEW: SAFE CONNECTOR FOR DISCOVERY PIPELINE
# ============================================================

def prepare_receptors_for_genes(
    genes: list,
    force: bool = False
):
    """
    Prepare docking receptors for multiple gene targets.

    ✔ Used by DiscoveryAgent
    ✔ Safe batch processing
    """

    results = {}

    for gene in genes:
        results[gene] = prepare_receptor(
            gene=gene,
            force=force
        )

    return results
