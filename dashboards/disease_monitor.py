import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import os

# ============================================================
# PAGE CONFIG (ONLY ONCE)
# ============================================================
st.set_page_config(
    page_title="Disease Monitor Dashboard",
    layout="wide"
)

# ============================================================
# HEADER
# ============================================================
st.title("🧠 Disease Monitor Dashboard")
st.caption("GNN-based Disease–Gene–Compound Intelligence")

# ============================================================
# BACKEND CONFIG
# ============================================================
API_URL = "http://127.0.0.1:8000"

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.subheader("⚙️ System Status")

    if os.getenv("MONGODB_URI"):
        st.success("✅ MongoDB configured")
    else:
        st.warning("⚠️ MongoDB not configured")

    st.markdown("---")
    st.subheader("📦 Modules")
    st.write("• FastAPI (GNN + RAG)")
    st.write("• ChEMBL Live")
    st.write("• PubMed Live")
    st.write("• Plotly Network")

# ============================================================
# DISEASE SELECTION
# ============================================================
DISEASES = [
    "Alzheimer's disease",
    "Parkinson's disease",
    "Huntington's disease",
    "Amyotrophic lateral sclerosis",
    "Multiple sclerosis",
    "Pancreatic cancer"
]

disease = st.selectbox("Select disease", DISEASES)

run = st.button("🚀 Run Disease Monitor")

if not run:
    st.stop()

# ============================================================
# CALL FASTAPI
# ============================================================
with st.spinner("Running GNN + Retrieval pipeline..."):
    response = requests.get(
        f"{API_URL}/disease_monitor",
        params={"disease": disease},
        timeout=120
    )

if response.status_code != 200:
    st.error("❌ FastAPI error")
    st.stop()

data = response.json()

# ============================================================
# PARSE RESPONSE
# ============================================================
ranked_targets = data.get("ranked_targets", [])
graph = data.get("graph", {})
rag_ready = data.get("rag_ready", True)

if not ranked_targets:
    st.warning("⚠️ No genes extracted from abstracts.")
    st.stop()

df = pd.DataFrame(ranked_targets)

# ============================================================
# TOP TARGETS TABLE
# ============================================================
st.subheader("🧬 Top Ranked Gene Targets (GNN)")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# INTERACTIVE NETWORK GRAPH (PLOTLY)
# ============================================================
st.subheader("🕸️ Disease–Gene–Compound Network")

nodes = graph.get("nodes", [])
edges = graph.get("edges", [])

if nodes and edges:
    node_x, node_y, node_text, node_color = [], [], [], []

    for n in nodes:
        node_x.append(n["x"])
        node_y.append(n["y"])
        node_text.append(n["id"])
        node_color.append(
            "red" if n["type"] == "gene"
            else "blue" if n["type"] == "compound"
            else "green"
        )

    edge_x, edge_y = [], []
    for e in edges:
        edge_x += [e["x0"], e["x1"], None]
        edge_y += [e["y0"], e["y1"], None]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=1, color="#888"),
        hoverinfo="none"
    ))

    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        marker=dict(
            size=14,
            color=node_color,
            line=dict(width=2)
        )
    ))

    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Graph data not available.")

# ============================================================
# RAG EXPLANATIONS (FROM FASTAPI)
# ============================================================
st.subheader("📚 RAG-based Target Explanations")

TOP_K = 5
top_nodes = df.head(TOP_K)

for _, row in top_nodes.iterrows():
    with st.expander(f"🧬 {row['node']} (score: {row['score']:.3f})"):
        rag_resp = requests.get(
            f"{API_URL}/rag_explain",
            params={
                "gene": row["node"],
                "disease": disease
            }
        )
        if rag_resp.status_code == 200:
            st.write(rag_resp.json()["explanation"])
        else:
            st.warning("RAG explanation unavailable.")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("Powered by GNNs · ChEMBL · PubMed · BioNER · RAG · FastAPI")
