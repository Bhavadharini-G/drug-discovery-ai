# 🧬 Drug Discovery & Disease Monitoring AI System

🔗 Live Application  
👉 https://drug-discovery-ai-pink.vercel.app/

---

## 📌 Project Overview

The Drug Discovery & Disease Monitoring AI System is a unified AI-driven biomedical intelligence platform that integrates drug discovery and disease monitoring into a single end-to-end workflow.

The system enables researchers to explore disease mechanisms, prioritize disease-associated gene targets, evaluate drug-like compounds, and analyze biomedical research trends using modern AI, bioinformatics, and graph-based learning techniques.

---

## 🎯 Problem Statement

Traditional drug discovery and disease analysis pipelines are often:
- Time-consuming and fragmented across tools  
- Difficult to interpret due to massive biomedical datasets  
- Lacking integrated, evidence-based decision support  

This project addresses these challenges by combining literature mining, graph learning, pathway analysis, compound scoring, and structural validation into one unified workflow.

---

## 🧪 System Modules

### Drug Discovery Engine
- Disease / gene / compound-driven discovery  
- PubMed-based literature mining  
- Target identification and prioritization  
- AlphaFold protein structure mapping  
- Pathway enrichment analysis  
- Compound evaluation using Activity, QSAR, and ADMET  
- Evidence-backed AI explanations  

### Disease Monitoring Engine
- Disease-focused gene prioritization  
- Graph Neural Network (GNN)-based gene ranking  
- Disease–gene interaction network  
- Publication timeline visualization (year-wise trends)  
- Data-driven analysis instead of generic summaries  

---

## ⚙️ Methodology

1. User query ingestion (disease / gene / compound)  
2. Biomedical literature extraction (PubMed)  
3. Target identification and filtering  
4. GNN-based disease–gene scoring  
5. Protein structure and pathway analysis  
6. Compound retrieval and scoring  
7. Evidence-grounded result aggregation  
8. Structure-based molecular docking validation  

---

## 🧠 Algorithms & Techniques

- Natural Language Processing (NLP)  
- Biomedical Transformers (BioBERT, PubMedBERT)  
- Graph Neural Networks (GNN)  
- QSAR modeling (descriptor-based)  
- ADMET rule-based heuristics  
- Pathway enrichment statistics  
- Retrieval-Augmented Reasoning (RAG)  

---

## 🛠️ Tech Stack

Backend: FastAPI, Python, MongoDB  
AI / Bioinformatics: BioBERT, PubMedBERT, AlphaFold, ChEMBL, PubChem, GNN  
Frontend: React (Vite), Streamlit-like UI  
Deployment: Backend on Railway, Frontend on Vercel  

---

## 👥 Target Users

- Bioinformatics researchers  
- Drug discovery scientists  
- Academic R&D teams  
- Biomedical researchers  

---

## 🌟 Novelty & Innovation

- Unified drug discovery + disease monitoring platform  
- GNN-based disease–gene prioritization  
- Publication timeline instead of generic summaries  
- Multi-signal compound ranking (Activity + QSAR + ADMET)  
- End-to-end, interpretable AI workflow with docking validation  

---

## 🚀 How to Run Locally

Backend:
- conda create -n drugai python=3.10  
- conda activate drugai  
- pip install -r requirements.txt  
- uvicorn app.example_main:app --reload  

Frontend:
- cd frontend  
- npm install  
- npm run dev  

---

## 🧬 Molecular Docking Procedure (End-to-End)

This project includes a complete structure-based molecular docking pipeline using AutoDock Vina and PyMOL to validate AI-prioritized drug–target interactions.

Docking folder structure:
Docking_files/
- protein/protein.pdbqt  
- Ligand/ligand.pdbqt  
- config.txt  
- vina.exe  
- out.pdbqt  

Protein preparation:
- Protein structure obtained from AlphaFold or PDB  
- Water molecules removed  
- Polar hydrogens and charges added  
- Saved as protein.pdbqt  

Ligand preparation:
- Ligand retrieved from PubChem or ChEMBL  
- Converted to 3D structure  
- Hydrogens and Gasteiger charges added  
- Saved as ligand.pdbqt  

Grid box definition:
- Binding site defined using AutoDockTools  
- Grid center and size reused for Vina docking  

Vina configuration (config.txt):
receptor = protein/protein.pdbqt  
ligand = Ligand/ligand.pdbqt  
center_x = X  
center_y = Y  
center_z = Z  
size_x = 22.5  
size_y = 22.5  
size_z = 22.5  
exhaustiveness = 8  
num_modes = 9  
energy_range = 3  

Run docking:
- vina.exe --config config.txt --out out.pdbqt  

Docking results:
- Binding affinity (ΔG, kcal/mol) printed in terminal  
- Most negative score indicates strongest binding  
- Mode 1 corresponds to the best docking pose  

Visualization in PyMOL:
- load protein/protein.pdbqt  
- load out.pdbqt  
- split_states out  
- enable protein and out_0001  
- protein shown as cartoon, ligand as sticks  

---

## 📌 Summary

An end-to-end AI-powered biomedical intelligence platform integrating literature-driven drug discovery, graph-based disease monitoring, multi-signal compound prioritization, and full molecular docking validation, designed for academic research and early-stage drug discovery.
