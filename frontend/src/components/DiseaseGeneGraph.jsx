import ForceGraph2D from "react-force-graph-2d";

export default function DiseaseGeneGraph({ graph }) {
  if (!graph || !graph.nodes || graph.nodes.length === 0) {
    return <p>No graph data available.</p>;
  }

  const data = {
    nodes: graph.nodes.map(n => ({
      id: n.id,
      type: n.type
    })),
    links: graph.edges.map(e => ({
      source: e.source,
      target: e.target
    }))
  };

  return (
    <div
      style={{
        height: "520px",
        background: "#f8fafc",
        borderRadius: "12px",
        border: "1px solid #e2e8f0"
      }}
    >
      <ForceGraph2D
        graphData={data}
        nodeLabel="id"
        nodeRelSize={6}
        linkColor={() => "#94a3b8"}
        nodeColor={node =>
          node.type === "disease" ? "#dc2626" : "#2563eb"
        }
        d3Force="charge"
        d3Charge={-200}
      />
    </div>
  );
}
