# 🧬 Drug Discovery & Disease Monitoring AI System

## 📌 Project Overview
This project is a **unified AI-driven platform** that integrates **Drug Discovery** and **Disease Monitoring** into a single system.  
It enables researchers to explore disease mechanisms, prioritize gene targets, evaluate drug-like compounds, and analyze research trends using modern AI and bioinformatics techniques.

---

## 🎯 Problem Statement
Traditional drug discovery and disease analysis are:
- Time-consuming and fragmented across tools
- Difficult to interpret due to large biomedical datasets
- Lacking integrated decision support

This system addresses these challenges by combining **literature mining, graph learning, pathway analysis, and compound scoring** into one workflow.

---

## 🧪 System Modules

### 1️⃣ Drug Discovery Engine
- Disease / target / compound–driven discovery
- PubMed-based literature mining
- Target identification and prioritization
- AlphaFold protein structure mapping
- Pathway enrichment analysis
- Compound evaluation using **Activity, QSAR, and ADMET**
- Evidence-backed AI explanations

### 2️⃣ Disease Monitoring Engine
- Disease-centric monitoring system
- Gene ranking using **Graph Neural Networks (GNN)**
- Disease–gene interaction network
- **Publication timeline visualization** (year-wise research trends)
- Replaced RAG text explanations with quantitative literature trends

---

## ⚙️ Methodology (High Level)
1. User query ingestion (disease / gene / compound)
2. Biomedical literature extraction (PubMed)
3. Target identification and filtering
4. GNN-based target scoring (Disease Monitor)
5. Structure and pathway analysis
6. Compound retrieval and scoring
7. Evidence-grounded result aggregation

---

## 🧠 Algorithms & Techniques Used
- Natural Language Processing (NLP)
- Biomedical Transformers (BioBERT / PubMedBERT)
- Graph Neural Networks (GNN)
- QSAR modeling (descriptor-based)
- ADMET rule-based heuristics
- Pathway enrichment statistics
- Retrieval-Augmented reasoning

---

## 🛠️ Tech Stack
**Backend**
- FastAPI
- Python
- MongoDB

**AI / Bioinformatics**
- BioBERT / PubMedBERT
- AlphaFold
- ChEMBL / PubChem
- Pathway enrichment tools
- Graph Neural Networks

**Frontend**
- React (Vite)
- Streamlit-like UI behavior

**Deployment**
- Backend: Railway
- Frontend: Vercel

---

## 👥 Target Users
- Bioinformatics researchers
- Drug discovery scientists
- Academic&D / academic researchers

---

## 🌟 Novelty & Innovation
- Unified drug discovery + disease monitoring system
- GNN-based disease–gene prioritization
- Publication timeline instead of generic text summaries
- Multi-signal compound ranking (Activity + QSAR + ADMET)
- End-to-end, interpretable AI workflow

---

## 🚀 How to Run (Local)

### Backend
```bash
uvicorn app.example_main:app --reload
