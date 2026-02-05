# network_driven_workflow.py

from agents.discovery_agent import DiscoveryAgent
from agents.design_agent import DesignAgent
from agents.validation_agent import ValidationAgent
from agents.approval_agent import ApprovalAgent
from tools.network import build_disease_network, run_gnn_analysis
from tools.kegg_pathway import get_pathways_from_kegg
from tools.chembl_target import get_chembl_compounds_for_target

# Example stub for pathway database interface
def get_pathways_stub(disease_name):
    # Replace with real pathway lookup (e.g., KEGG, Reactome)
    return [f"{disease_name}_pathway1", f"{disease_name}_pathway2"]

import matplotlib.pyplot as plt
import networkx as nx

def multi_target_workflow(disease_name, gene_list):
    # 1. Retrieve real pathways from KEGG
    pathways = get_pathways_from_kegg(disease_name)
    targets = gene_list

    # 2. Build disease network
    network = build_disease_network(pathways, targets)

    # 3. Run GNN/digital-twin analysis
    network_insights = run_gnn_analysis(network)

    # 4. Discover compounds for each target
    compound_results = {}
    for target in targets:
        print(f"[INFO] Retrieving compounds for target: {target}")
        compounds = get_chembl_compounds_for_target(target, max_results=1)
        print(f"[INFO] Found {len(compounds)} compounds for {target}")
        compound_results[target] = compounds

    # 5. Design and evaluate compounds (multi-compound, multi-target)
    design_results = {}
    # Cache agent objects to avoid repeated model loading
    design_agent = DesignAgent()
    validation_agent = ValidationAgent()
    approval_agent = ApprovalAgent()
    for target, compounds in compound_results.items():
        for compound in compounds:
            chembl_id = compound.get("chembl_id")
            if not chembl_id:
                continue
            print(f"[INFO] Running agents for target: {target}, compound: {chembl_id}")
            try:
                design = design_agent.run(chembl_id)
                print(f"[INFO] DesignAgent done for {chembl_id}")
            except Exception as e:
                print(f"[ERROR] DesignAgent failed for {chembl_id}: {e}")
                design = None
            try:
                validation = validation_agent.run(chembl_id)
                print(f"[INFO] ValidationAgent done for {chembl_id}")
            except Exception as e:
                print(f"[ERROR] ValidationAgent failed for {chembl_id}: {e}")
                validation = None
            try:
                approval = approval_agent.run(chembl_id)
                print(f"[INFO] ApprovalAgent done for {chembl_id}")
            except Exception as e:
                print(f"[ERROR] ApprovalAgent failed for {chembl_id}: {e}")
                approval = None
            design_results[(target, chembl_id)] = {
                "design": design,
                "validation": validation,
                "approval": approval,
                "compound_info": compound
            }

    # 6. Aggregate and rank results using network insights
    ranked_candidates = rank_candidates(design_results, network_insights)

    # Visualization 1: Disease network
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(network)
    node_colors = ["#1f77b4" if network.nodes[n]["type"] == "gene" else "#ff7f0e" for n in network.nodes]
    nx.draw(network, pos, with_labels=True, node_color=node_colors, edge_color="#cccccc", node_size=700, font_size=10)
    plt.title(f"Disease Network: {disease_name}")
    plt.show(block=True)

    # Visualization 2: Ranked candidates bar plot
    if ranked_candidates:
        plt.figure(figsize=(10, 5))
        labels = [f"{t}-{c}" for (t, c), _ in ranked_candidates]
        scores = [network_insights.get(t, 0) for (t, c), _ in ranked_candidates]
        plt.bar(labels, scores, color="#1f77b4")
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Network Vulnerability Score")
        plt.title("Ranked Candidate Compounds by Target")
        plt.tight_layout()
        plt.show(block=True)

    print("Workflow complete. You may close any plot windows.")
    
    return {
        "network": network,
        "network_insights": network_insights,
        "design_results": design_results,
        "ranked_candidates": ranked_candidates
    }

# Helper function to rank candidates based on network analysis
def rank_candidates(design_results, network_insights):
    # Example: prioritize compounds that target vulnerable nodes or synergistic pathways
    ranked = sorted(design_results.items(), key=lambda x: network_insights.get(x[0][0], 0), reverse=True)
    return ranked

# Example usage
if __name__ == "__main__":
    print("Enter a disease name (e.g., Parkinson disease, Type 2 diabetes, Breast cancer):")
    disease = input().strip()
    print("Enter comma-separated gene/protein targets (e.g., SNCA,LRRK2,PARK2,PINK1):")
    gene_list = [g.strip() for g in input().split(",") if g.strip()]
    results = multi_target_workflow(disease, gene_list)
    
    # Human-readable summary table of ranked candidates

    try:
        import pandas as pd
        ranked_candidates = results.get('ranked_candidates', [])
        network_insights = results.get('network_insights', {})
        table_rows = []
        for (target, compound), result in ranked_candidates:
            score = network_insights.get(target, None)
            compound_info = result.get('design', {}).get('compound_info', {})
            docking = result.get('design', {}).get('docking_result', '')
            qsar = result.get('design', {}).get('qsar_result', '')
            validation = result.get('validation', {}).get('lab_result', '')
            clinical = result.get('validation', {}).get('clinical_result', '')
            approval = result.get('approval', {}).get('approval_report', '')
            summary = result.get('design', {}).get('llm_summary', '')
            table_rows.append({
                'Target': target,
                'Compound': compound,
                'Score': score,
                'MW': compound_info.get('properties', {}).get('molecular_weight', ''),
                'Formula': compound_info.get('properties', {}).get('formula', ''),
                'Docking': docking,
                'QSAR': qsar,
                'Lab': validation,
                'Clinical': clinical,
                'Approval': approval,
                'Summary': summary.split('\n')[0] if summary else ''
            })
        df = pd.DataFrame(table_rows)
        print("\nRanked Candidate Summary Table:")
        print(df.to_string(index=False))
    except ImportError:
        print("pandas is not installed. Install pandas for table output.")
