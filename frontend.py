import streamlit as st
import requests
import re
import os
from datetime import datetime
from pymongo import MongoClient


st.title("🧬 Drug Discovery AI Assistant")

# =====================================================
# MongoDB (SAFE CONNECTION – NO BOOL CHECK BUG)
# =====================================================
@st.cache_resource
def get_mongo_collection():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        return None
    client = MongoClient(uri)
    db = client["drug_discovery"]
    return db["history"]

history_collection = get_mongo_collection()

# =====================================================
# Utility Functions
# =====================================================
def extract_alphafold_url(structure_msg):
    match = re.search(r"https://alphafold.ebi.ac.uk/entry/[^\s]+", structure_msg)
    return match.group(0) if match else None

def is_pdb_content(text):
    return isinstance(text, str) and text.startswith("HEADER") and "ATOM" in text

def save_history(query, qtype, result):
    if history_collection is not None:
        history_collection.insert_one({
            "query": query,
            "query_type": qtype,
            "timestamp": datetime.utcnow(),
            "result": result
        })

# =====================================================
# Disease List
# =====================================================
disease_list = [
    "Alzheimer's disease",
    "Parkinson's disease",
    "Amyotrophic lateral sclerosis (ALS)",
    "Pancreatic cancer",
    "Breast cancer",
    "Lung cancer",
    "Diabetes mellitus",
    "COVID-19",
    "Rheumatoid arthritis",
    "Multiple sclerosis",
    "Huntington's disease",
    "Ovarian cancer",
    "Glioblastoma",
    "Leukemia",
    "Prostate cancer"
]

# =====================================================
# SECTION 1: DISEASE
# =====================================================
st.header("1️⃣ Disease-Driven Discovery")
col1, col2 = st.columns([2, 3])

with col1:
    selected_disease = st.selectbox(
        "Select a disease",
        ["(Choose a disease)"] + disease_list
    )

with col2:
    disease_input = st.text_input(
        "Or enter a disease name",
        value=selected_disease if selected_disease != "(Choose a disease)" else ""
    )

if st.button("🔍 Submit Disease Query"):
    response = requests.get(
        f"http://127.0.0.1:8000/full_workflow",
        params={"query": disease_input}
    )
    if response.status_code == 200:
        result = response.json()
        save_history(disease_input, "disease", result)

        st.subheader("Disease Output")
        discovery = result.get("discovery", {})

        # AlphaFold
        structure_msg = discovery.get("structure")
        if structure_msg:
            if is_pdb_content(structure_msg):
                st.download_button(
                    "⬇️ Download AlphaFold PDB",
                    data=structure_msg,
                    file_name=f"{disease_input}.pdb",
                    mime="chemical/x-pdb"
                )
            else:
                af_url = extract_alphafold_url(structure_msg)
                if af_url:
                    st.markdown(f"[🔗 Download AlphaFold Structure]({af_url})")

        st.json(result)

# =====================================================
# SECTION 2: TARGET
# =====================================================
st.header("2️⃣ Target-Driven Discovery")
target_input = st.text_input("Enter target (gene/protein)", placeholder="BACE1")

if st.button("🎯 Submit Target Query"):
    response = requests.get(
        f"http://127.0.0.1:8000/full_workflow",
        params={"query": target_input}
    )
    if response.status_code == 200:
        result = response.json()
        save_history(target_input, "target", result)
        st.subheader("Target Output")
        st.json(result)

# =====================================================
# SECTION 3: COMPOUND
# =====================================================
st.header("3️⃣ Compound-Driven Discovery")
compound_input = st.text_input("Enter compound", placeholder="aspirin")

if st.button("💊 Submit Compound Query"):
    response = requests.get(
        f"http://127.0.0.1:8000/full_workflow",
        params={"query": compound_input}
    )
    if response.status_code == 200:
        result = response.json()
        save_history(compound_input, "compound", result)

        st.subheader("Compound Output")
        discovery = result.get("discovery", {})

        structure_msg = discovery.get("structure")
        if structure_msg:
            af_url = extract_alphafold_url(structure_msg)
            if af_url:
                st.markdown(f"[🔗 AlphaFold Structure]({af_url})")

        st.json(result)

# =====================================================
# SIDEBAR: MONGODB STATUS + HISTORY
# =====================================================
st.sidebar.header("🗄 MongoDB")

if history_collection is None:
    st.sidebar.error("❌ MongoDB not connected")
else:
    st.sidebar.success("✅ MongoDB connected")

    if st.sidebar.checkbox("🔐 Admin: View History"):
        docs = list(history_collection.find().sort("timestamp", -1).limit(20))
        for d in docs:
            with st.sidebar.expander(
                f"{d['query']} | {d['query_type']} | {d['timestamp']}"
            ):
                st.json(d["result"])
def main():
    # existing frontend.py code goes here
    pass

if __name__ == "__main__":
    main()
