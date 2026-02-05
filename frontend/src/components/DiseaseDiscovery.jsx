import { useState } from "react";

const API_URL = "http://127.0.0.1:8000";

const DISEASE_LIST = [
  "Alzheimer's disease","Parkinson's disease",
  "Amyotrophic lateral sclerosis (ALS)",
  "Pancreatic cancer","Breast cancer","Lung cancer",
  "Diabetes mellitus","COVID-19","Rheumatoid arthritis",
  "Multiple sclerosis","Huntington's disease",
  "Ovarian cancer","Glioblastoma","Leukemia","Prostate cancer"
];

export default function DrugDiscovery() {
  const [disease, setDisease] = useState("");
  const [target, setTarget] = useState("");
  const [compound, setCompound] = useState("");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [source, setSource] = useState(""); // which section triggered

  const runQuery = async (query, src) => {
    if (!query) return;
    setSource(src);
    setLoading(true);
    const res = await fetch(
      `${API_URL}/full_workflow?query=${encodeURIComponent(query)}`
    );
    setResult(await res.json());
    setLoading(false);
  };

  const discovery = result?.discovery || {};
  const design = result?.design || {};
  const validation = result?.validation || {};
  const approval = result?.approval || {};

  return (
    <div className="page">
      <h1>🧪 Drug Discovery AI Assistant</h1>
      <p className="subtitle">
        Three independent discovery modes with a unified AI workflow
      </p>

      {/* ===================== 1️⃣ DISEASE ===================== */}
      <section className="section-card">
        <h2><span className="step">1</span> Disease-Driven Discovery</h2>

        <label>Select a disease</label>
        <select value={disease} onChange={(e) => setDisease(e.target.value)}>
          <option value="">(Choose a disease)</option>
          {DISEASE_LIST.map(d => <option key={d}>{d}</option>)}
        </select>

        <label>Or enter a disease name</label>
        <input
          value={disease}
          onChange={(e) => setDisease(e.target.value)}
          placeholder="Breast cancer"
        />

        <button onClick={() => runQuery(disease, "Disease-Driven")}>
          🔍 Submit Disease Query
        </button>
      </section>

      {/* ===================== 2️⃣ TARGET ===================== */}
      <section className="section-card">
        <h2><span className="step">2</span> Target-Driven Discovery</h2>

        <label>Enter target (gene / protein)</label>
        <input
          value={target}
          onChange={(e) => setTarget(e.target.value)}
          placeholder="EGFR"
        />

        <button onClick={() => runQuery(target, "Target-Driven")}>
          🎯 Submit Target Query
        </button>
      </section>

      {/* ===================== 3️⃣ COMPOUND ===================== */}
      <section className="section-card">
        <h2><span className="step">3</span> Compound-Driven Discovery</h2>

        <label>Enter compound</label>
        <input
          value={compound}
          onChange={(e) => setCompound(e.target.value)}
          placeholder="Aspirin"
        />

        <button onClick={() => runQuery(compound, "Compound-Driven")}>
          💊 Submit Compound Query
        </button>
      </section>

      {loading && <p className="loading">Running discovery pipeline…</p>}

      {/* ===================== RESULTS ===================== */}
      {result && (
        <section className="result-card">
          <h2>✅ Results ({source})</h2>

          <div className="result-grid">
            {/* Discovery */}
            <div className="result-box discovery">
              <h3>🧬 Discovery</h3>
              <Info label="Literature (PMIDs)" value={discovery.literature?.join(", ")} />
              <Info label="Suggested Targets" value={discovery.suggested_targets?.join(", ")} />
              <Info label="LLM Summary" value={discovery.llm_summary} />
              <AlphaFold structure={discovery.structure} />
            </div>

            {/* Design */}
            <div className="result-box design">
              <h3>💊 Design</h3>
              <Info label="Docking" value={design.docking_result} />
              <Info label="QSAR / ADMET" value={design.qsar_result} />
              <Info label="LLM Summary" value={design.llm_summary} />
            </div>

            {/* Validation */}
            <div className="result-box validation">
              <h3>🧪 Validation</h3>
              <Info label="Lab Result" value={validation.lab_result} />
              <Info label="Clinical Result" value={validation.clinical_result} />
              <Info label="LLM Summary" value={validation.llm_summary} />
            </div>

            {/* Approval */}
            <div className="result-box approval">
              <h3>✔ Approval</h3>
              <Info label="Approval Report" value={approval.approval_report} />
              <Info label="LLM Summary" value={approval.llm_summary} />
            </div>
          </div>
        </section>
      )}
    </div>
  );
}

/* ================= HELPERS ================= */

function Info({ label, value }) {
  if (!value) return null;
  return (
    <div className="info-row">
      <span className="info-label">{label}</span>
      <p>{value}</p>
    </div>
  );
}

function AlphaFold({ structure }) {
  if (!structure) return null;
  const isLink = typeof structure === "string" && structure.startsWith("http");
  return (
    <div className="info-row">
      <span className="info-label">🧬 AlphaFold Structure</span>
      {isLink ? (
        <a href={structure} target="_blank" rel="noreferrer">
          🔗 View AlphaFold 3D Structure
        </a>
      ) : (
        <p>{structure}</p>
      )}
    </div>
  );
}
