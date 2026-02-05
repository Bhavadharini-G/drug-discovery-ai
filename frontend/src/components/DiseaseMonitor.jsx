import { useState } from "react";
import { runDiseaseMonitor } from "../api/api";
import TargetChart from "./TargetChart";

/* ================= DISEASE OPTIONS ================= */
const DISEASES = [
  "Alzheimer's disease",
  "Parkinson's disease",
  "Amyotrophic lateral sclerosis",
  "Huntington's disease",
  "Multiple sclerosis",
  "Pancreatic cancer",
  "Breast cancer",
  "Lung cancer",
  "Glioblastoma",
  "Ovarian cancer"
];

export default function DiseaseMonitor() {
  const [disease, setDisease] = useState(DISEASES[0]);
  const [targets, setTargets] = useState([]);
  const [timeline, setTimeline] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /* ================= RUN MONITOR ================= */
  const runMonitor = async () => {
    if (!disease) return;

    setLoading(true);
    setError(null);
    setTargets([]);
    setTimeline({});

    try {
      const data = await runDiseaseMonitor(disease);

      const safeTargets = Array.isArray(data?.ranked_targets)
        ? data.ranked_targets
        : [];

      setTargets(safeTargets);
      setTimeline(data?.evidence_timeline ?? {});
    } catch (e) {
      console.error(e);
      setError("Failed to load disease monitor results.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1>🧠 Disease Monitor Dashboard</h1>
      <p className="subtitle">
        GNN-based disease–gene prioritization with longitudinal evidence trends
      </p>

      {/* ================= INPUT ================= */}
      <div className="section-card">
        <label>Select disease</label>

        <select value={disease} onChange={(e) => setDisease(e.target.value)}>
          {DISEASES.map((d) => (
            <option key={d}>{d}</option>
          ))}
        </select>

        <button onClick={runMonitor}>
          🚀 Run Disease Monitor
        </button>
      </div>

      {loading && <p>⏳ Running GNN pipeline…</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* ================= OUTPUT ================= */}
      {targets.length > 0 && (
        <>
          {/* ===== TABLE ===== */}
          <div className="section-card">
            <h3>🧬 Ranked Gene Targets</h3>

            <table className="compound-table">
              <thead>
                <tr>
                  <th>Gene</th>
                  <th>GNN Score</th>
                </tr>
              </thead>
              <tbody>
                {targets.map((t) => (
                  <tr key={t.node}>
                    <td>{t.node}</td>
                    <td>{Number(t.score).toFixed(4)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* ===== BAR CHART ===== */}
          <div className="section-card chart-box">
            <h3>📊 Target Importance</h3>
            <TargetChart data={targets} />
          </div>

          {/* ===== EVIDENCE TIMELINE ===== */}
          <div className="section-card">
            <h3>📈 Evidence Timeline (Publications Over Time)</h3>

            {Object.keys(timeline).length === 0 && (
              <p>No publication timeline available.</p>
            )}

            {Object.entries(timeline).map(([gene, points]) => (
              <div key={gene} style={{ marginBottom: "18px" }}>
                <strong>{gene}</strong>
                <div
                  style={{
                    fontFamily: "monospace",
                    marginTop: "6px",
                    whiteSpace: "nowrap"
                  }}
                >
                  {points.map((p) => (
                    <span key={p.year} style={{ marginRight: "10px" }}>
                      {p.year}: {"▇".repeat(Math.min(p.count, 6))}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
