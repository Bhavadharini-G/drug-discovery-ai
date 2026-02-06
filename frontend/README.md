# 🧬 Drug Discovery & Disease Monitoring AI System

🔗 **Live Application**:  
👉 https://drug-discovery-ai-pink.vercel.app/

---

## 📌 Project Overview

The **Drug Discovery & Disease Monitoring AI System** is a unified, AI-driven biomedical intelligence platform that integrates **drug discovery** and **disease monitoring** into a single end-to-end workflow.

The system enables researchers and scientists to:
- Explore disease mechanisms  
- Prioritize disease-associated gene targets  
- Evaluate drug-like compounds  
- Analyze biomedical research trends  

by leveraging **modern AI**, **bioinformatics**, and **graph-based learning techniques**.

---

## 🎯 Problem Statement

Traditional drug discovery and disease analysis pipelines are often:

- ⏳ Time-consuming and fragmented across multiple tools  
- 📚 Difficult to interpret due to massive biomedical literature  
- ❌ Lacking integrated, evidence-based decision support  

This project addresses these challenges by providing a **single, interpretable, AI-powered platform** that combines literature mining, graph learning, pathway analysis, and compound scoring into a cohesive workflow.

---

## 🧪 System Modules

### 1️⃣ Drug Discovery Engine

A target- and compound-centric AI pipeline designed to support early-stage drug discovery.

**Key Capabilities:**
- Disease / gene / compound-driven discovery
- PubMed-based biomedical literature mining
- Target identification and prioritization
- **AlphaFold** protein structure mapping
- Biological pathway enrichment analysis
- Compound evaluation using:
  - Activity scoring  
  - QSAR descriptors  
  - ADMET heuristics
- Evidence-backed AI explanations

---

### 2️⃣ Disease Monitoring Engine

A disease-centric monitoring system focused on **quantitative, graph-based insights**.

**Key Capabilities:**
- Disease-focused gene prioritization
- **Graph Neural Network (GNN)**-based gene ranking
- Disease–gene interaction network construction
- Publication timeline visualization  
  (year-wise research trends)
- Replaces verbose RAG explanations with **data-driven literature trends**

---

## ⚙️ Methodology (High-Level Workflow)

1. User query ingestion (disease / gene / compound)
2. Biomedical literature extraction (PubMed)
3. Target identification and filtering
4. **GNN-based disease–gene scoring**
5. Protein structure and pathway analysis
6. Compound retrieval and scoring
7. Evidence-grounded result aggregation

---

## 🧠 Algorithms & Techniques Used

- **Natural Language Processing (NLP)**
- **Biomedical Transformers**
  - BioBERT
  - PubMedBERT
- **Graph Neural Networks (GNN)**
- **QSAR modeling** (descriptor-based)
- **ADMET rule-based heuristics**
- **Pathway enrichment statistics**
- **Retrieval-Augmented Reasoning (RAG)**

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- Python
- MongoDB

### AI / Bioinformatics
- BioBERT / PubMedBERT
- AlphaFold
- ChEMBL
- PubChem
- Pathway enrichment tools
- Graph Neural Networks

### Frontend
- React (Vite)
- Streamlit-like interactive UI behavior

### Deployment
- **Backend**: Railway  
- **Frontend**: Vercel  

---

## 👥 Target Users

- Bioinformatics researchers  
- Drug discovery scientists  
- Academic R&D teams  
- Biomedical researchers  

---

## 🌟 Novelty & Innovation

- Unified **drug discovery + disease monitoring** platform
- **GNN-based disease–gene prioritization**
- Publication timeline analysis instead of generic text summaries
- Multi-signal compound ranking:
  - Activity + QSAR + ADMET
- End-to-end, interpretable AI workflow
- Research-grade, modular system architecture

---

## 🚀 How to Run Locally

### Backend

```bash
uvicorn app.example_main:app --reload
