import Plot from "react-plotly.js";

export default function TargetChart({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <Plot
      data={[
        {
          x: data.map(d => d.node),
          y: data.map(d => d.score),
          type: "bar",
          marker: { color: "#2E86C1" }
        }
      ]}
      layout={{
        title: "Target Importance (GNN Scores)",
        height: 450,
        margin: { t: 50, l: 50, r: 20, b: 100 }
      }}
      style={{ width: "100%" }}
    />
  );
}
