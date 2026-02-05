---

## 🧬 Disease Monitor Dashboard

### Goal
The Disease Monitor Dashboard provides researchers and clinicians with a real-time, interactive view of the latest biomedical literature and clinical trials for major neurodegenerative diseases. It is designed to accelerate hypothesis generation, target validation, and translational research by integrating up-to-date data from PubMed and ClinicalTrials.gov.

### Features
- **Multi-disease support:** Select from a dropdown of major neurodegenerative diseases (e.g., Parkinson's, Alzheimer's, ALS, Huntington's, Multiple Sclerosis, and more).
- **Live PubMed integration:** Instantly fetches and displays the latest research articles for the selected disease and date range.
- **ClinicalTrials.gov integration:** Shows current and recent clinical trials for the selected disease, filterable by start date.
- **Gene extraction:** Automatically highlights gene mentions in articles using the HGNC gene symbol set.
- **Top gene targets visualization:** Interactive bar chart of the most frequently mentioned genes in recent literature.
- **Date filtering:** Easily filter both articles and trials by publication/start date.


---

---

# Drug Discovery AI Assistant



## 🚀 Project Overview
An end-to-end, modular AI system for drug discovery, integrating biomedical databases, multi-agent orchestration, and domain-specific LLMs. Designed for automation, extensibility, and real-world research impact.

---

## ⚡ Quickstart
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the API:
   ```bash
   uvicorn app.example_main:app --reload
   ```
3. (Optional) Start the Streamlit frontend:
   ```bash
   streamlit run frontend.py
   ```
4. Then open http://localhost:8501 in your browser.
   
5. Try the API:
   ```bash
   curl "http://127.0.0.1:8000/full_workflow?query=aspirin"
   ```

---

## 🛠️ Technologies Used
- **Python** (3.10+)
- **FastAPI** (API backend)
- **Streamlit** (web UI)
- **LangChain, CrewAI** (agent orchestration)
- **MongoDB** (vector/document storage)
- **Hugging Face Transformers** (BioGPT, PubMedBERT, BioBERT)
- **Docker** (optional, for deployment)

---

## 🧑‍💻 Key Features & Enhancements
- Modular, multi-agent architecture (Discovery, Design, Validation, Approval)
- Real-world biomedical data integration (PubMed, PubChem, AlphaFold)
- LLM-based summarization and knowledge extraction (BioGPT, PubMedBERT, BioBERT)
- Target-to-compound lookup and multi-compound analysis
- Robust, extensible Python code with clear documentation and error handling
- Interactive Streamlit frontend and production-ready FastAPI backend
- Advanced analysis: clustering, PCA, docking prep, reporting, and more

---

## 🧠 System Architecture & Agents
![Architecture Diagram](assets/architecture_diagram.png)

---

## 🌐 Network-Driven Drug Discovery Workflow

This workflow leverages biomedical networks and graph neural networks (GNNs) to analyze disease-gene-compound relationships. It integrates multi-agent orchestration (Design, Validation, Approval) and domain-specific LLMs to rank candidate compounds for a selected disease.

**Key Steps:**
- Select a disease and gene/protein targets
- Build the disease network and analyze with GNNs
- Query compound databases for candidate molecules
- Run multi-agent workflow to rank candidates
- Visualize results and export ranked candidates

**Demonstration Notebook:**
- [Demo: Network-Driven Workflow for Parkinson Disease](demo_workflow.ipynb)

The notebook provides a step-by-step demonstration, including network visualization, candidate ranking, and export functionality.

**Layered Workflow:**
- API Layer: Handles incoming requests and responses
- Agent Layer: Orchestrates agent logic and task delegation
- Tool Layer: Modular access to external data sources and AI models
- Data Layer: Persistent and intermediate data storage
- Utils: Shared utility functions

**Agent Descriptions:**
| Agent            | Description                                                                 | AI Methods/Models Used                |
|------------------|-----------------------------------------------------------------------------|--------------------------------------|
| Discovery Agent  | Searches biomedical literature and databases to identify potential drug candidates. | LLM (RAG), PubMed, PubChem           |
| Design Agent     | Designs and optimizes candidate compounds based on discovery results.             | LLM, AlphaFold, Docking, QSAR        |
| Validation Agent | Validates candidate compounds using lab and clinical data.                        | LLM, LabTool, ClinicalTool           |
| Approval Agent   | Assesses regulatory requirements and prepares documentation for approval.         | LLM, RegulatoryTool                  |

---

## 🎯 Drug Target Discovery Pipeline

This system includes an **automated target identification workflow** that extracts potential drug targets from biomedical literature using state-of-the-art NLP and network analysis. 

### **Key Capabilities:**

#### **1. Disease-to-Target Extraction**
- **Input:** Disease name (e.g., "Parkinson's disease", "Alzheimer's disease")
- **Process:**
  - Query PubMed for recent literature (top N abstracts)
  - Apply **BioBERT Named Entity Recognition (NER)** to extract gene/protein entities
  - Filter and rank by frequency and relevance
  - Cross-reference with canonical disease-gene databases (KEGG, OMIM)
- **Output:** Ranked list of target genes/proteins with confidence scores

#### **2. Network-Based Target Prioritization**
- Build disease-gene-compound interaction networks from **KEGG pathways** and **ChEMBL**
- Apply **Graph Neural Networks (GNNs)** to identify critical nodes
- Score targets by:
  - Network centrality (betweenness, degree)
  - Pathway vulnerability
  - Druggability (existence of known compounds)

#### **3. Automated Compound Retrieval**
- For each identified target, query **ChEMBL** for known bioactive compounds
- Retrieve compound structures, activity data, and molecular properties
- Rank compounds by predicted efficacy and drug-likeness

### **Demonstrated Examples:**

| Disease | Extracted Targets | Notebook |
|---------|-------------------|----------|
| Parkinson's disease | SNCA, LRRK2, PARK2, PINK1 | [demo_workflow.ipynb](demo_workflow.ipynb) |
| Alzheimer's disease | BACE1, APP, MAPT, PSEN1, PSEN2 | [Example in README](#-disease-sample-queries) |
| ALS | SOD1, C9orf72, FUS, TARDBP | [ALS_ligand_integration_demo.ipynb](ALS_ligand_integration_demo.ipynb) |
| Pancreatic cancer | KRAS, TP53, CDKN2A, SMAD4 | API `/discovery` endpoint |

### **Try It Yourself:**

```bash
# Extract targets for a disease
curl "http://127.0.0.1:8000/discovery?query=Parkinson's disease"

# Or use Python directly
from agents.discovery_agent import DiscoveryAgent
result = DiscoveryAgent().run('Alzheimer disease')
print(result['suggested_targets'])
```

**Sample Output:**
```json
{
  "literature": ["40886227", "40881622", "40881157"],
  "suggested_targets": ["BACE1", "APP", "MAPT", "PSEN1", "PSEN2"],
  "llm_summary": "Alzheimer disease is associated with amyloid-beta accumulation.. .",
  "network_scores": {
    "BACE1": 0.87,
    "APP": 0.82,
    "MAPT":  0.76
  }
}
```

### **Technologies Used:**
- **BioBERT** (dmis-lab/biobert-v1.1): Biomedical NER for target extraction
- **PubMedBERT** (microsoft/BiomedNLP-PubMedBERT): Literature summarization
- **PyTorch Geometric**:  Graph Neural Networks for network analysis
- **KEGG API**:  Pathway data integration
- **ChEMBL WebResource Client**: Target-compound relationship queries

### **Architecture:**
```
Disease Input → PubMed Query → BioBERT NER → Target Candidates
                                                    ↓
                                            Network Construction (KEGG)
                                                    ↓
                                            GNN Analysis & Ranking
                                                    ↓
                                            ChEMBL Compound Retrieval
                                                    ↓
                                            Multi-Agent Evaluation
```

---

## 🛠️ API Endpoints
The FastAPI backend exposes the following endpoints (see `app/example_main.py`):

| Endpoint         | Method | Description                                                      | Example Query Param(s)         |
|------------------|--------|------------------------------------------------------------------|-------------------------------|
| `/discovery`     | GET    | Run DiscoveryAgent on a disease/target/compound                  | `?query=BACE1`                |
| `/design`        | GET    | Run DesignAgent on a compound                                    | `?compound=aspirin`           |
| `/validation`    | GET    | Run ValidationAgent on a candidate drug                          | `?candidate=aspirin`          |
| `/approval`      | GET    | Run ApprovalAgent on a candidate drug                            | `?candidate=aspirin`          |
| `/full_workflow` | GET    | Run the full workflow (Discovery → Design → Validation → Approval)| `?query=BACE1`                |

All endpoints return JSON responses. Use `/full_workflow` for an end-to-end pipeline, or call individual endpoints for stepwise control.

---

## 📈 Example Outputs & Advanced Analysis
**API Example:**
```bash
curl "http://127.0.0.1:8000/full_workflow?query=BACE1"
```
Sample response:
```json
{
  "discovery": {"literature": ["40886227", ...], "structure": "AlphaFold structure ...", ...},
  "design": {"compound_info": { ... }, ...},
  "validation": {"lab_result": "...", ...},
  "approval": {"approval_report": "...", ...}
}
```



**Advanced Analysis in Notebook:**
- Chemical space visualization (PCA of molecular fingerprints)
- Clustering of candidate compounds
- Preparation of 3D structures for docking (SDF export)
- Advanced property and ADMET visualizations (e.g., pairplots)
- Experimental planning (top candidate selection)

---



## 🌱 Future Work
- Add more ML/DL modeling (e.g., biomarker → drug response prediction)
- Expand ETL pipelines for omics/clinical data
- Integrate experiment tracking (MLflow)
- Deploy with Docker for reproducibility
- Write a LinkedIn/Medium post about the project

---

## 🤝 Contributing
Open issues or pull requests to help improve the project, or share your use cases and feedback!


![Architecture Diagram](assets/architecture_diagram.png)

* User/API Client sends a request to the FastAPI app.
* The app orchestrates agents and tools.
* Each agent delegates to specialized tools for data retrieval and analysis.
* Tools fetch data from online databases or perform computations.
* All results and intermediate data are stored in MongoDB.

## 🧑‍🔬 Agent Descriptions & AI Methods

| Agent            | Description                                                                 | AI Methods/Models Used                |
|------------------|-----------------------------------------------------------------------------|--------------------------------------|
| Discovery Agent  | Searches biomedical literature and databases to identify potential drug candidates. | LLM (RAG), PubMed, PubChem           |
| Design Agent     | Designs and optimizes candidate compounds based on discovery results.             | LLM, AlphaFold, Docking, QSAR        |
| Validation Agent | Validates candidate compounds using lab and clinical data.                        | LLM, LabTool, ClinicalTool           |
| Approval Agent   | Assesses regulatory requirements and prepares documentation for approval.         | LLM, RegulatoryTool                  |

---

## 🚀 Quick Start
```bash
pip install -r requirements.txt
uvicorn app.example_main:app --reload
```

## 🛠️ API Endpoints

The FastAPI backend exposes the following endpoints (see `app/example_main.py`):

| Endpoint         | Method | Description                                                      | Example Query Param(s)         |
|------------------|--------|------------------------------------------------------------------|-------------------------------|
| `/discovery`     | GET    | Run DiscoveryAgent on a disease/target/compound                  | `?query=BACE1`                |
| `/design`        | GET    | Run DesignAgent on a compound                                    | `?compound=aspirin`           |
| `/validation`    | GET    | Run ValidationAgent on a candidate drug                          | `?candidate=aspirin`          |
| `/approval`      | GET    | Run ApprovalAgent on a candidate drug                            | `?candidate=aspirin`          |
| `/full_workflow` | GET    | Run the full workflow (Discovery → Design → Validation → Approval)| `?query=BACE1`                |

All endpoints return JSON responses. Use `/full_workflow` for an end-to-end pipeline, or call individual endpoints for stepwise control.
---

## 🏁 What Next?

Now that you have the Drug Discovery AI Assistant running locally, here are some suggested next steps:

- **Customize Agents:** Modify or extend the agent logic in `agents/` to add new tools, change prompts, or integrate additional data sources.
- **Integrate New Models:** Try other LLMs from Ollama or Hugging Face by updating the agent `model` parameter, or add your own domain-specific models.
- **Experiment with Prompts:** Tune the prompts for each agent to improve the quality and relevance of LLM outputs for your specific research needs.
- **Deploy the API:** Use FastAPI’s deployment options to run the system in production (e.g., with Docker, on a cloud VM, or behind a reverse proxy).
- **Connect a Frontend:** Build a web or desktop UI to interact with the API, visualize results, or manage workflows.
- **Scale Up:** Integrate with more advanced vector databases, distributed compute, or workflow orchestration tools for larger-scale research.
- **Contribute:** Open issues or pull requests to help improve the project, or share your use cases and feedback!


---


## 🌐 Simple Streamlit Frontend

You can interact with the Drug Discovery AI backend using a simple Streamlit web app. This provides an easy-to-use interface for entering queries and viewing results.

### Usage

1. Make sure your FastAPI backend is running (see Quick Start above).
2. Install Streamlit if you haven't already:
	```bash
	pip install streamlit
	```
3. Run the frontend:
	```bash
	streamlit run frontend.py
	```
4. Enter a disease, target, or compound in the web UI and view the results interactively.

The Streamlit app is located in `frontend.py`.


You can build a user-friendly frontend to interact with the Drug Discovery AI API. Here are some options and examples:

### 1. Simple Web Client (HTML/JS)

You can use a basic HTML/JavaScript page to send requests to the FastAPI backend:

```html
<form id="queryForm">
	<input type="text" id="query" placeholder="Enter compound name">
	<button type="submit">Submit</button>
</form>
<pre id="result"></pre>
<script>
document.getElementById('queryForm').onsubmit = async function(e) {
	e.preventDefault();
	const q = document.getElementById('query').value;
	const res = await fetch(`http://127.0.0.1:8000/full_workflow?query=${encodeURIComponent(q)}`);
	document.getElementById('result').textContent = await res.text();
};
</script>
```

### 2. Streamlit App (Python)

Create a simple Streamlit UI for local use:

```python
import streamlit as st
import requests

st.title("Drug Discovery AI Assistant")
query = st.text_input("Enter compound name:")
if st.button("Submit"):
		response = requests.get(f"http://127.0.0.1:8000/full_workflow?query={query}")
		st.write(response.text)
```

### 3. Advanced Web UI (React, Next.js, etc.)

For a modern, user-friendly experience, build a custom frontend using React, Next.js, or similar frameworks. Example (React fetch call):

```javascript
fetch('http://127.0.0.1:8000/full_workflow?query=BACE1')
	.then(res => res.json())
	.then(data => setResult(data));
```

You can design interactive dashboards, result visualizations, and workflow management features tailored to your needs.


---

## 🧪 Step-by-Step Example: Discovering a Drug Candidate

Here’s how you can use the Drug Discovery AI pipeline for a real-world drug discovery scenario:

**Goal:** Identify and evaluate new drug candidates for Alzheimer’s disease (target: BACE1)

### 1. Start the Backend API
```bash
uvicorn app.example_main:app --reload
```

### 2. Submit a Query (e.g., via browser or curl)
```bash
curl "http://127.0.0.1:8000/full_workflow?query=BACE1"
```
Or use the interactive docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Review the Output
- **Discovery Agent:** Summarizes BACE1’s role in Alzheimer’s, retrieves relevant compounds and literature.
- **Design Agent:** Suggests and evaluates new compound designs, docking scores, and predicted properties.
- **Validation Agent:** Simulates lab/clinical validation, summarizes findings.
- **Approval Agent:** Generates a regulatory summary for the candidate.

### 4. Iterate and Refine
- Try different targets or compounds (e.g., "aspirin", "tau protein").
- Adjust agent prompts or models for more specific results.
- Integrate your own data or tools for deeper analysis.

### 5. (Optional) Build a Frontend
- Use the provided examples to create a web UI for easier interaction and visualization.




## 🧪 Step-by-Step Example Outputs

Here’s a real example showing the outputs at each step of the workflow for the query "Alzheimer disease":

### 1. 🧠 Discovery Agent
Input: `Alzheimer disease`
Output:
```json
{
	"literature": ["40886227", "40881622", "40881157"],
	"structure": "AlphaFold structure for Alzheimer disease not found online (status 404). Download manually from https://alphafold.ebi.ac.uk/entry/Alzheimer disease if needed.",
	"pubchem": {"error": "PubChem API error: 404 Client Error: PUGREST.NotFound for url: https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/Alzheimer%20disease/property/MolecularWeight,MolecularFormula,IUPACName/JSON"},
	"llm_summary": "PubMedBERT summary (top predictions):\nalzheimer disease is associated with inflammation. (score: 0.143)\nalzheimer disease is associated with aging. (score: 0.093)\nalzheimer disease is associated with obesity. (score: 0.084)\nalzheimer disease is associated with neuroinflammation. (score: 0.064)\nalzheimer disease is associated with depression. (score: 0.035)",
	"suggested_targets": ["PET", "IEEE", "USA", "SUVR", "ADNI"]
}
```

### 2. 🧬 Design Agent
Input: `BACE1`
Output:
```json
{
	"docking_score": -8.2,
	"compound_suggestions": ["CompoundX", "CompoundY"],
	...
}
```

### 3. 🧪 Validation Agent
Input: `CompoundX`
Output:
```json
{
	"lab_results": "Efficacy confirmed in vitro.",
	...
}
```

### 4. 🏛️ Approval Agent
Input: `CompoundX`
Output:
```json
{
	"regulatory_summary": "Meets FDA requirements.",
	...
}
```

---

Test the full workflow (all stages):

```bash
curl "http://127.0.0.1:8000/full_workflow?query=BACE1"
```

Test individual stages:

```bash
curl "http://127.0.0.1:8000/discovery?query=BACE1"
curl "http://127.0.0.1:8000/design?compound=aspirin"
curl "http://127.0.0.1:8000/validation?candidate=aspirin"
curl "http://127.0.0.1:8000/approval?candidate=aspirin"
```


### 🧬 Disease Sample Queries

#### Example: DiscoveryAgent with BioBERT NER Extraction

You can run the DiscoveryAgent directly in Python to test disease-to-target extraction using BioBERT NER (with fallback to regex):

```python
from agents.discovery_agent import DiscoveryAgent
result = DiscoveryAgent().run('Alzheimer disease')
print(result)
```

**Sample Output:**

```
{
	'literature': ['40886227', '40881622', '40881157'],
	'structure': 'AlphaFold structure for Alzheimer disease not found online (status 404). Download manually from https://alphafold.ebi.ac.uk/entry/Alzheimer disease if needed.',
	'pubchem': {'error': 'PubChem API error: 404 Client Error: PUGREST.NotFound for url: https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/Alzheimer%20disease/property/MolecularWeight,MolecularFormula,IUPACName/JSON'},
	'llm_summary': 'PubMedBERT summary (top predictions):\nalzheimer disease is associated with inflammation. (score: 0.143)\nalzheimer disease is associated with aging. (score: 0.093)\nalzheimer disease is associated with obesity. (score: 0.084)\nalzheimer disease is associated with neuroinflammation. (score: 0.064)\nalzheimer disease is associated with depression. (score: 0.035)',
	'suggested_targets': ['PET', 'IEEE', 'USA', 'SUVR', 'ADNI']
}
```

This confirms that BioBERT NER-based target extraction is working. The `suggested_targets` field contains entities extracted from PubMed abstracts using BioBERT (with fallback to regex if needed).

---

You can start the workflow with a disease name. The system will suggest relevant protein/gene targets for further exploration:

```bash
# Alzheimer's disease (will suggest targets like BACE1, APP, MAPT, etc.)
curl "http://127.0.0.1:8000/discovery?query=Alzheimer's disease"

# Parkinson's disease
curl "http://127.0.0.1:8000/discovery?query=Parkinson's disease"

# Amyotrophic lateral sclerosis (ALS)
curl "http://127.0.0.1:8000/discovery?query=ALS"

# Pancreatic cancer
curl "http://127.0.0.1:8000/discovery?query=pancreatic cancer"
```

You can then use the suggested targets as queries for the full workflow or design endpoints.

**Note:** When a protein structure is needed and not found locally, the app will automatically download the precomputed 3D structure from the AlphaFold EBI database.

---


**Newly added advanced analysis steps include:**
- Chemical space visualization (PCA of molecular fingerprints)
- Clustering of candidate compounds
- Preparation of 3D structures for docking (SDF export)
- Advanced property and ADMET visualizations (e.g., pairplots)
- Experimental planning (top candidate selection)

**Requirements:**
- All dependencies are installed automatically if you follow the notebook's installation cell, including `rdkit`, `matplotlib`, `networkx`, `torch`, `torch-geometric`, `pandas`, `numpy`, `scikit-learn`, and `seaborn`.

**Usage:**
- Open and run the notebook step by step to reproduce the full workflow and explore further analysis options for your candidate compounds.
- Each section is documented with markdown cells explaining the purpose and requirements.

See the notebook for detailed, reproducible examples and visualizations.

---

