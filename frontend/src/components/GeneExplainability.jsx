export default function GeneExplainability({ score, explanation }) {
  if (!explanation) return null;

  const safeScore =
    typeof score === "number" && !isNaN(score) ? score : 0;

  return (
    <div
      style={{
        marginTop: "12px",
        padding: "15px",
        background: "#f1f5f9",
        borderLeft: "4px solid #2563eb",
        borderRadius: "6px"
      }}
    >
      <p>
        <strong>🔬 GNN Score:</strong>{" "}
        {safeScore.toFixed(3)}
      </p>

      <p style={{ marginTop: "8px" }}>
        <strong>📚 RAG Explanation:</strong>
      </p>

      <p style={{ whiteSpace: "pre-wrap", lineHeight: "1.6" }}>
        {explanation}
      </p>
    </div>
  );
}
