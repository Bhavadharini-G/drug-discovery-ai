"""
chem_utils.py: Shared cheminformatics utility functions for property calculation and drug-likeness filtering.
"""
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, Lipinski, rdMolDescriptors

def lipinski_filter(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False
    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd = Descriptors.NumHDonors(mol)
    hba = Descriptors.NumHAcceptors(mol)
    return (mw <= 500 and logp <= 5 and hbd <= 5 and hba <= 10)

def calc_admet_properties(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    props = {}
    props['MW'] = Descriptors.MolWt(mol)
    props['LogP'] = Crippen.MolLogP(mol)
    props['HBD'] = Lipinski.NumHDonors(mol)
    props['HBA'] = Lipinski.NumHAcceptors(mol)
    props['RotB'] = Lipinski.NumRotatableBonds(mol)
    props['TPSA'] = rdMolDescriptors.CalcTPSA(mol)
    return props
