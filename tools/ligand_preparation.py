# ============================================================
# LIGAND PREPARATION (SMILES → PDBQT)
# ============================================================

import os
import shutil
import subprocess
from rdkit import Chem
from rdkit.Chem import AllChem

# NEW: compound loader connection
from tools.compound_loader import load_compounds, load_compounds_for_target


# ============================================================
# PATH CONFIGURATION (PROJECT-SAFE)
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LIGAND_DIR = os.path.join(BASE_DIR, "data", "ligands")
TMP_DIR = os.path.join(BASE_DIR, "data", "tmp")

os.makedirs(LIGAND_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)


# ============================================================
# FIND AutoDockTools SCRIPT
# ============================================================

def find_prepare_ligand():
    """
    Locate prepare_ligand4.py safely.
    """
    candidates = [
        "prepare_ligand4.py",
        shutil.which("prepare_ligand4.py"),
        shutil.which("prepare_ligand"),
    ]

    for c in candidates:
        if c and os.path.exists(c):
            return c

    raise RuntimeError(
        "❌ prepare_ligand4.py not found.\n"
        "Install AutoDockTools and ensure it is on PATH."
    )


PREPARE_LIGAND = find_prepare_ligand()


# ============================================================
# CORE FUNCTION
# ============================================================

def smiles_to_pdbqt(smiles: str, ligand_name: str, force: bool = False):
    """
    Convert SMILES → 3D PDBQT for docking

    Returns:
        dict:
        {
          "status": "ok" | "error",
          "path": str | None,
          "message": str
        }
    """

    pdbqt_path = os.path.join(LIGAND_DIR, f"{ligand_name}.pdbqt")

    if os.path.exists(pdbqt_path) and not force:
        return {
            "status": "ok",
            "path": pdbqt_path,
            "message": "Ligand already prepared"
        }

    # --------------------------------------------------------
    # 1️⃣ SMILES → RDKit molecule
    # --------------------------------------------------------
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {
            "status": "error",
            "path": None,
            "message": f"Invalid SMILES: {smiles}"
        }

    mol = Chem.AddHs(mol)

    # --------------------------------------------------------
    # 2️⃣ 3D embedding
    # --------------------------------------------------------
    try:
        if AllChem.EmbedMolecule(mol, AllChem.ETKDG()) != 0:
            AllChem.EmbedMolecule(mol)
        AllChem.UFFOptimizeMolecule(mol)
    except Exception as e:
        return {
            "status": "error",
            "path": None,
            "message": f"RDKit embedding failed: {e}"
        }

    # --------------------------------------------------------
    # 3️⃣ Write temporary MOL
    # --------------------------------------------------------
    mol_file = os.path.join(TMP_DIR, f"{ligand_name}.mol")
    Chem.MolToMolFile(mol, mol_file)

    # --------------------------------------------------------
    # 4️⃣ MOL → PDBQT (AutoDockTools)
    # --------------------------------------------------------
    try:
        cmd = [
            PREPARE_LIGAND,
            "-l", mol_file,
            "-o", pdbqt_path,
            "-A", "hydrogens"
        ]

        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=True
        )

        if os.path.exists(pdbqt_path):
            return {
                "status": "ok",
                "path": pdbqt_path,
                "message": "Ligand prepared successfully"
            }

    except Exception as e:
        return {
            "status": "error",
            "path": None,
            "message": f"prepare_ligand4.py failed: {e}"
        }

    return {
        "status": "error",
        "path": None,
        "message": "Unknown ligand preparation error"
    }


# ============================================================
# 🔗 NEW: PREPARE LIGANDS FROM CSV (SYSTEM CONNECTION)
# ============================================================

def prepare_ligands_for_target(
    gene: str,
    limit: int = 5,
    force: bool = False
):
    """
    Prepare ligands (PDBQT) for a specific gene target.

    ✔ Reads from ligands_for_docking.csv
    ✔ Uses SMILES
    ✔ Safe for DiscoveryAgent
    """

    prepared = []

    compounds = load_compounds_for_target(gene, limit=limit)

    for c in compounds:
        name = c.get("name")
        smiles = c.get("smiles")

        if not name or not smiles:
            continue

        result = smiles_to_pdbqt(
            smiles=smiles,
            ligand_name=name,
            force=force
        )

        prepared.append({
            "compound": name,
            "result": result
        })

    return prepared


# ============================================================
# BATCH MODE (GENERIC)
# ============================================================

def batch_prepare_ligands(smiles_dict: dict):
    """
    Convert multiple SMILES → PDBQT
    """
    results = {}

    for name, smiles in smiles_dict.items():
        results[name] = smiles_to_pdbqt(smiles, name)

    return results
