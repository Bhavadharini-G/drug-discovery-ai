import AlphaFoldSection from "./AlphaFoldSection";

export default function DrugDiscoveryResult({ result }) {
  if (!result) return null;

  const { discovery, design, validation, approval } = result;

  return (
    <div className="result-grid">

      {/* ================= DISCOVERY ================= */}
      <div className="result-card discovery">
        <h3>🧬 Discovery</h3>

        {discovery.literature && (
          <Info
            label="Literature Evidence (PMIDs)"
            value={discovery.literature.join(", ")}
          />
        )}

        {discovery.suggested_targets && (
          <Info
            label="Suggested Targets"
            value={discovery.suggested_targets.join(", ")}
          />
        )}

        {discovery.llm_summary && (
          <Info
            label="LLM Insight"
            value={discovery.llm_summary}
          />
        )}

        {/* 🔴 ALPHAFOLD HANDLED HERE */}
        <AlphaFoldSection structure={discovery.structure} />
      </div>

      {/* ================= DESIGN ================= */}
      <div className="result-card design">
        <h3>💊 Design</h3>

        <Info label="Docking Result" value={design.docking_result} />
        <Info label="QSAR / ADMET" value={design.qsar_result} />
        <Info label="LLM Insight" value={design.llm_summary} />
      </div>

      {/* ================= VALIDATION ================= */}
      <div className="result-card validation">
        <h3>🧪 Validation</h3>

        <Info label="Lab Evidence" value={validation.lab_result} />
        <Info label="Clinical Evidence" value={validation.clinical_result} />
        <Info label="LLM Insight" value={validation.llm_summary} />
      </div>

      {/* ================= APPROVAL ================= */}
      <div className="result-card approval">
        <h3>✔ Approval</h3>

        <Info
          label="Approval Report"
          value={approval.approval_report}
        />

        <Info
          label="LLM Insight"
          value={approval.llm_summary}
        />
      </div>
    </div>
  );
}

/* ---------- Helper ---------- */
function Info({ label, value }) {
  if (!value) return null;

  return (
    <div className="info-row">
      <span className="info-label">{label}</span>
      <p>{value}</p>
    </div>
  );
}
