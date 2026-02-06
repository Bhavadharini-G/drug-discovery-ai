# 🧬 Drug Discovery & Disease Monitoring AI System

🔗 **Live Application**  
👉 https://drug-discovery-ai-pink.vercel.app/

---

## 📌 Project Overview

The **Drug Discovery & Disease Monitoring AI System** is a unified AI-driven biomedical intelligence platform that integrates **drug discovery** and **disease monitoring** into a single end-to-end workflow.

The system enables researchers to explore disease mechanisms, prioritize disease-associated gene targets, evaluate drug-like compounds, and analyze biomedical research trends using modern **AI**, **bioinformatics**, and **graph-based learning techniques**.

---

## 🎯 Problem Statement

Traditional drug discovery and disease analysis pipelines are often:

- Time-consuming and fragmented across tools  
- Difficult to interpret due to massive biomedical datasets  
- Lacking integrated, evidence-based decision support  

This project addresses these challenges by combining literature mining, graph learning, pathway analysis, and compound scoring into one unified workflow.

---

## 🧪 System Modules

### 1️⃣ Drug Discovery Engine

Target- and compound-centric AI pipeline for early-stage drug discovery.

**Key Features**
- Disease / gene / compound-driven discovery
- PubMed-based literature mining
- Target identification and prioritization
- AlphaFold protein structure mapping
- Pathway enrichment analysis
- Compound evaluation using Activity, QSAR, and ADMET
- Evidence-backed AI explanations

---

### 2️⃣ Disease Monitoring Engine

Disease-centric monitoring system focused on quantitative insights.

**Key Features**
- Disease-focused gene prioritization
- Graph Neural Network (GNN)-based gene ranking
- Disease–gene interaction network
- Publication timeline visualization (year-wise trends)
- Data-driven analysis instead of generic text summaries

---

## ⚙️ Methodology

1. User query ingestion (disease / gene / compound)
2. Biomedical literature extraction (PubMed)
3. Target identification and filtering
4. GNN-based disease–gene scoring
5. Protein structure and pathway analysis
6. Compound retrieval and scoring
7. Evidence-grounded result aggregation

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

**Backend**
- FastAPI
- Python
- MongoDB

**AI / Bioinformatics**
- BioBERT / PubMedBERT
- AlphaFold
- ChEMBL
- PubChem
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
- Academic R&D teams  
- Biomedical researchers  

---

## 🌟 Novelty & Innovation

- Unified drug discovery + disease monitoring platform
- GNN-based disease–gene prioritization
- Publication timeline instead of generic summaries
- Multi-signal compound ranking (Activity + QSAR + ADMET)
- End-to-end, interpretable AI workflow

---

## 🚀 How to Run Locally

```bash
# Backend
conda create -n drugai python=3.10
conda activate drugai
pip install -r requirements.txt
uvicorn app.example_main:app --reload

# Frontend
cd frontend
npm install
npm run dev
