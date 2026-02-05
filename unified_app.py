from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime
from pymongo import MongoClient

API_URL = "http://127.0.0.1:8000"

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Drug Discovery AI – Unified System",
    layout="wide"
)

# ============================================================
# MONGODB (SAFE)
# ============================================================
@st.cache_resource
def get_history():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        return None
    try:
        c = MongoClient(uri, serverSelectionTimeoutMS=5000)
        c.admin.command("ping")
        return c["drug_discovery"]["history"]
    except Exception:
        return None

history = get_history()

# ============================================================
# UTILS
# ============================================================
def save_history(q, t, r):
    if history is not None:
        try:
            history.insert_one({
                "query": q,
                "query_type": t,
                "timestamp": datetime.utcnow(),
                "result": r
            })
        except Exception:
            pass

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("🧬 Drug Discovery AI")

module = st.sidebar.radio(
    "Select Module",
    ["🧪 Drug Discovery Assistant", "🧠 Disease Monitor Dashboard"]
)

st.sidebar.markdown("---")
if history is not None:
    st.sidebar.success("✅ MongoDB connected")
else:
    st.sidebar.warning("⚠️ MongoDB not connected")

if history is not None and st.sidebar.checkbox("🔐 Admin: View History"):
    docs = list(history.find().sort("timestamp", -1).limit(20))
    for d in docs:
        with st.sidebar.expander(
            f"{d.get('query','')} | {d.get('query_type','')} | {d.get('timestamp','')}"
        ):
            st.json(d.get("result", {}))

# ============================================================
# MODULE 1 — DRUG DISCOVERY (3 SECTIONS)
# ============================================================
if module == "🧪 Drug Discovery Assistant":
    st.title("🧬 Drug Discovery AI Assistant")
    st.caption("Disease-Driven • Target-Driven • Compound-Driven Discovery")

    disease_list = [
        "Alzheimer's disease","Parkinson's disease",
        "Amyotrophic lateral sclerosis (ALS)",
        "Pancreatic cancer","Breast cancer","Lung cancer",
        "Diabetes mellitus","COVID-19","Rheumatoid arthritis",
        "Multiple sclerosis","Huntington's disease",
        "Ovarian cancer","Glioblastoma","Leukemia","Prostate cancer"
    ]

    # ====================================================
    # 1️⃣ DISEASE-DRIVEN DISCOVERY
    # ====================================================
    st.header("1️⃣ Disease-Driven Discovery")

    col1, col2 = st.columns([2, 3])
    with col1:
        selected_disease = st.selectbox(
            "Select disease",
            [""] + disease_list
        )
    with col2:
        disease = st.text_input(
            "Or enter disease name",
            value=selected_disease
        )

    if st.button("🔍 Run Disease Discovery"):
        r = requests.get(f"{API_URL}/full_workflow", params={"query": disease})
        data = r.json()
        save_history(disease, "disease", data)

        discovery = data.get("discovery", {})
        genes = discovery.get("suggested_targets", [])

        st.subheader("🧬 Suggested Targets")
        st.write(genes)

        st.subheader("🧬 AlphaFold Structures")
        for g in genes[:5]:
            af = requests.get(f"{API_URL}/alphafold/{g}").json()
            if isinstance(af.get("structure"), str):
                st.download_button(
                    f"⬇️ Download {g} PDB",
                    af["structure"],
                    file_name=f"{g}.pdb"
                )
            else:
                st.link_button(
                    f"🔎 Search AlphaFold for {g}",
                    "https://alphafold.ebi.ac.uk/"
                )

        st.subheader("📄 Full Output")
        st.json(data)

    st.divider()

    # ====================================================
    # 2️⃣ TARGET-DRIVEN DISCOVERY
    # ====================================================
    st.header("2️⃣ Target-Driven Discovery")

    target = st.text_input(
        "Enter gene / protein target",
        placeholder="BACE1 / TP53 / EGFR"
    )

    if st.button("🎯 Run Target Discovery"):
        r = requests.get(f"{API_URL}/full_workflow", params={"query": target})
        data = r.json()
        save_history(target, "target", data)

        st.subheader("📄 Full Output")
        st.json(data)

    st.divider()

    # ====================================================
    # 3️⃣ COMPOUND-DRIVEN DISCOVERY
    # ====================================================
    st.header("3️⃣ Compound-Driven Discovery")

    compound = st.text_input(
        "Enter compound name",
        placeholder="Aspirin / Imatinib / Gemcitabine"
    )

    if st.button("💊 Run Compound Discovery"):
        r = requests.get(f"{API_URL}/full_workflow", params={"query": compound})
        data = r.json()
        save_history(compound, "compound", data)

        st.subheader("📄 Full Output")
        st.json(data)

# ============================================================
# MODULE 2 — DISEASE MONITOR DASHBOARD
# ============================================================
if module == "🧠 Disease Monitor Dashboard":
    st.title("🧠 Disease Monitor Dashboard")
    st.caption("GNN-based Disease–Gene–Evidence Intelligence")

    DISEASES = [
        "Alzheimer's disease","Parkinson's disease",
        "Huntington's disease","Amyotrophic lateral sclerosis",
        "Multiple sclerosis","Pancreatic cancer",
        "Breast cancer","Lung cancer","Glioblastoma"
    ]

    disease = st.selectbox("Select disease", DISEASES)

    if st.button("🚀 Run Disease Monitor"):
        r = requests.get(f"{API_URL}/disease_monitor", params={"disease": disease})
        data = r.json()
        save_history(disease, "disease_monitor", data)

        df = pd.DataFrame(data.get("ranked_targets", []))

        st.subheader("🧬 Ranked Gene Targets")
        st.dataframe(df, use_container_width=True)

        # -------------------------------
        # GNN BAR CHART
        # -------------------------------
        st.subheader("📊 Target Importance (GNN Scores)")
        if not df.empty:
            fig = go.Figure(go.Bar(
                x=df["node"],
                y=df["score"],
                marker_color="#2E86C1"
            ))
            fig.update_layout(
                height=450,
                xaxis_title="Gene",
                yaxis_title="GNN Score"
            )
            st.plotly_chart(fig, use_container_width=True)

        # -------------------------------
        # RAG EXPLANATIONS
        # -------------------------------
        st.subheader("📚 RAG-based Explanations")
        for g in df["node"].head(5):
            with st.expander(g):
                rr = requests.get(
                    f"{API_URL}/rag_explain",
                    params={"gene": g, "disease": disease}
                )
                st.write(rr.json().get("explanation"))

        # -------------------------------
        # PATHWAY ENRICHMENT
        # -------------------------------
        st.subheader("🧬 Pathway Enrichment (KEGG)")
        pw = requests.post(
            f"{API_URL}/pathways",
            json={"genes": df["node"].head(10).tolist()}
        ).json()

        if pw.get("pathways"):
            st.dataframe(pd.DataFrame(pw["pathways"]), use_container_width=True)

        # -------------------------------
        # CLINICAL TRIALS
        # -------------------------------
        st.subheader("🧪 Clinical Trials Evidence")
        for g in df["node"].head(3):
            ct = requests.get(
                f"{API_URL}/clinical_trials",
                params={"query": g}
            ).json()

            trials = ct.get("trials", [])
            if trials:
                st.markdown(f"**{g}**")
                st.dataframe(pd.DataFrame(trials), use_container_width=True)
