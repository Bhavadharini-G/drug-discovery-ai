import { useState } from "react";
import { runFullWorkflow } from "../api/api";

export default function DrugDiscovery() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  /* ================= RUN PIPELINE ================= */
  const runDiscovery = async (q) => {
    if (!q) return;

    setLoading(true);
    setResult(null);

    try {
      const data = await runFullWorkflow(q);
      setResult(data);
    } catch (e) {
      console.error(e);
      alert("FastAPI error – check backend");
    } finally {
      setLoading(false);
    }
  };

  /* ================= SAFE DATA ================= */
  const discovery = result?.discovery ?? {};
  const targets = discovery.suggested_targets ?? [];
  const structures = discovery.structures ?? {};
  const pathways = Array.isArray(discovery.pathways)
    ? discovery.pathways
    : [];
  const geneScores = discovery.gene_compound_scores ?? {};
  const summary = discovery.llm_summary ?? "";

  return (
    <div className="page">
      <h1>🧪 Drug Discovery AI Assistant</h1>

      {/* ================= DISEASE ================= */}
      <div className="section-card">
        <h2>1️⃣ Disease-Driven Discovery</h2>

        <input
          placeholder="Enter disease name (e.g. Alzheimer's disease)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <button onClick={() => runDiscovery(query)}>
          🔍 Run Disease Discovery
        </button>
      </div>

      {/* ================= TARGET ================= */}
      <div className="section-card">
        <h2>2️⃣ Target-Driven Discovery</h2>

        <input
          placeholder="Enter gene / protein (e.g. BACE1)"
          onChange={(e) => setQuery(e.target.value)}
        />

        <button onClick={() => runDiscovery(query)}>
          🎯 Run Target Discovery
        </button>
      </div>

      {loading && <p>⏳ Running discovery pipeline…</p>}

      {/* ================= RESULTS ================= */}
      {result && (
        <div className="result-box">
          <h2>✅ Discovery Results</h2>
          <p><b>Query:</b> {query}</p>

          {/* TARGETS */}
          <h3>🧬 Suggested Targets</h3>
          {targets.length === 0 ? (
            <p>No targets found.</p>
          ) : (
            <ul>
              {targets.map((g) => (
                <li key={g}>{g}</li>
              ))}
            </ul>
          )}

          {/* ALPHAFOLD */}
          <h3>🧬 AlphaFold Structures</h3>
          {Object.keys(structures).length === 0 ? (
            <p>No structures available.</p>
          ) : (
            Object.entries(structures).map(([gene, info]) => (
              <p key={gene}>
                <b>{gene}</b>{" "}
                <a href={info?.manual_link} target="_blank" rel="noreferrer">
                  (manual)
                </a>
              </p>
            ))
          )}

          {/* PATHWAYS */}
          <h3>🧬 Pathway Enrichment</h3>
          {pathways.length === 0 ? (
            <p>No pathway enrichment found.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Pathway</th>
                  <th>P-value</th>
                  <th>Genes</th>
                </tr>
              </thead>
              <tbody>
                {pathways.map((p, i) => (
                  <tr key={i}>
                    <td>{p.pathway}</td>
                    <td>{Number(p.p_value).toExponential(2)}</td>
                    <td>{p.genes.join(", ")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {/* GENE → COMPOUND */}
          <h3>🧪 Gene → Compound Scores</h3>

          {Object.entries(geneScores).map(([gene, compounds]) => (
            <div key={gene} style={{ marginBottom: "24px" }}>
              <h4>{gene}</h4>

              {!compounds || compounds.length === 0 ? (
                <p>No compounds found.</p>
              ) : (
                <table>
                  <thead>
                    <tr>
                      <th>Compound</th>
                      <th>Activity</th>
                      <th>ADMET</th>
                      <th>QSAR</th>
                      <th>Final Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    {compounds.slice(0, 5).map((c, i) => (
                      <tr key={i}>
                        <td>{c.compound_name}</td>
                        <td>{c.activity}</td>
                        <td>{c.admet}</td>
                        <td>{c.qsar_score}</td>
                        <td>{c.final_score}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          ))}

          {/* SUMMARY */}
          <h3>📄 LLM Summary</h3>
          <pre style={{ whiteSpace: "pre-wrap" }}>
            {summary}
          </pre>
        </div>
      )}
    </div>
  );
}