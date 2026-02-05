import { useState } from "react";
import { runRAG } from "../api/api";

export default function RAGExplanation({ gene, disease }) {
  const [text, setText] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadExplanation = async () => {
    setLoading(true);
    const res = await runRAG(gene, disease);

    // 🔴 SAME LOGIC AS STREAMLIT: rr.json()["explanation"]
    setText(res.explanation.explanation);

    setLoading(false);
  };

  return (
    <div className="rag-container">
      {!text && (
        <button
          className="rag-btn"
          onClick={loadExplanation}
        >
          📚 Explain (Why this gene?)
        </button>
      )}

      {loading && (
        <p className="rag-loading">
          Fetching biomedical evidence…
        </p>
      )}

      {text && (
        <div className="rag-card">
          <h4>🧬 Why is <span>{gene}</span> important?</h4>
          <p>{text}</p>
        </div>
      )}
    </div>
  );
}
