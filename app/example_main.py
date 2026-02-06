from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# =========================================================
# ENV
# =========================================================
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

mongo_client = None
history_collection = None

# =========================================================
# AGENTS
# =========================================================
from agents.discovery_agent import DiscoveryAgent
from agents.design_agent import DesignAgent
from agents.validation_agent import ValidationAgent
from agents.approval_agent import ApprovalAgent

# =========================================================
# TOOLS
# =========================================================
from tools.disease_monitor_core import run_disease_monitor
from tools.gnn_model import run_gnn

# ENGINES
from tools.alphafold import AlphaFoldTool
from tools.admet_predictor import predict_admet
from tools.clinical_trials import get_trials_for_query
from tools.pathway_enrichment import run_pathway_enrichment

# =========================================================
# APP
# =========================================================
app = FastAPI(title="Drug Discovery AI Backend")

# =========================================================
# ✅ CORS — FINAL FIX (NO WILDCARDS)
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",

        # 🔥 EXACT VERCEL FRONTEND URL
        "https://drug-discovery-ai-pink.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# AGENT INSTANCES
# =========================================================
discovery_agent = DiscoveryAgent()
design_agent = DesignAgent()
validation_agent = ValidationAgent()
approval_agent = ApprovalAgent()

# =========================================================
# MONGO SAFE SERIALIZER (TORCH OPTIONAL)
# =========================================================
def mongo_safe(obj):
    try:
        import torch
        if isinstance(obj, torch.Tensor):
            return obj.detach().cpu().tolist()
    except Exception:
        pass

    if isinstance(obj, dict):
        return {k: mongo_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [mongo_safe(v) for v in obj]
    if isinstance(obj, tuple):
        return [mongo_safe(v) for v in obj]
    return obj

# =========================================================
# STARTUP — MONGODB
# =========================================================
@app.on_event("startup")
def startup_db():
    global mongo_client, history_collection

    if not MONGODB_URI:
        print("❌ MONGODB_URI not set")
        return

    try:
        mongo_client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000
        )
        mongo_client.admin.command("ping")
        history_collection = mongo_client["drug_discovery"]["history"]
        print("✅ MongoDB connected")
    except Exception as e:
        print("❌ MongoDB connection error:", e)
        history_collection = None

# =========================================================
# ROOT
# =========================================================
@app.get("/")
def root():
    return {"status": "Drug Discovery AI backend running"}

# =========================================================
# FULL WORKFLOW
# =========================================================
@app.get("/full_workflow")
def full_workflow(query: str):
    try:
        discovery = discovery_agent.run(query)

        discovery.setdefault("suggested_targets", [])
        discovery.setdefault("structures", {})
        discovery.setdefault("pathways", [])
        discovery.setdefault("gene_compound_scores", {})
        discovery.setdefault("llm_summary", "")

        result = {"discovery": discovery}

        if history_collection is not None:
            history_collection.insert_one({
                "query": query,
                "query_type": "full_workflow",
                "timestamp": datetime.utcnow(),
                "result": mongo_safe(result)
            })

        return result

    except Exception as e:
        print("❌ FULL WORKFLOW ERROR:", e)
        return {
            "discovery": {
                "suggested_targets": [],
                "structures": {},
                "pathways": [],
                "gene_compound_scores": {},
                "llm_summary": "Backend error occurred."
            }
        }

# =========================================================
# DISEASE MONITOR
# =========================================================
@app.get("/disease_monitor")
def disease_monitor(disease: str):
    monitor = run_disease_monitor(disease)

    genes = monitor.get("genes", [])
    evidence_timeline = monitor.get("evidence_timeline", {})

    if not genes:
        return {
            "ranked_targets": [],
            "graph": {},
            "evidence_timeline": {},
            "rag_ready": False
        }

    ranked_genes = run_gnn(genes, disease)

    nodes = [{"id": disease, "type": "disease"}]
    edges = []

    for g in ranked_genes:
        nodes.append({"id": g["gene"], "type": "gene"})
        edges.append({"source": disease, "target": g["gene"]})

    response = {
        "ranked_targets": [
            {"node": g["gene"], "score": g["score"]}
            for g in ranked_genes
        ],
        "graph": {
            "nodes": nodes,
            "edges": edges
        },
        "evidence_timeline": evidence_timeline,
        "rag_ready": False
    }

    if history_collection is not None:
        history_collection.insert_one({
            "query": disease,
            "query_type": "disease_monitor",
            "timestamp": datetime.utcnow(),
            "result": mongo_safe(response)
        })

    return response

# =========================================================
# ADMIN HISTORY
# =========================================================
@app.get("/admin/history")
def get_history(limit: int = 20):
    if history_collection is None:
        return []

    docs = history_collection.find().sort("timestamp", -1).limit(limit)
    results = []

    for d in docs:
        d["_id"] = str(d["_id"])
        results.append(d)

    return results

# =========================================================
# ENGINE ENDPOINTS
# =========================================================
@app.get("/alphafold/{gene}")
def alphafold_structure(gene: str):
    af = AlphaFoldTool()
    return {"gene": gene, "structure": af.predict(gene)}

@app.post("/admet")
def admet(payload: dict):
    return {
        "compound": payload.get("compound"),
        "admet_score": predict_admet(payload.get("compound"))
    }

@app.post("/pathways")
def pathways(payload: dict):
    return {
        "pathways": run_pathway_enrichment(payload.get("genes", []))
    }

@app.get("/clinical_trials")
def clinical_trials(query: str):
    return {
        "query": query,
        "trials": get_trials_for_query(query)
    }
