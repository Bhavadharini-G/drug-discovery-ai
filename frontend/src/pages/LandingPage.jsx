export default function LandingPage({ onSelect }) {
  return (
    <div className="landing">
      <div className="section-card center">
        <h2>Welcome</h2>
        <p>Select a module to begin</p>

        <div style={{ display: "flex", gap: "16px", marginTop: "24px", justifyContent: "center" }}>
          <button onClick={() => onSelect("discovery")}>
            🧪 Drug Discovery Assistant
          </button>

          <button onClick={() => onSelect("monitor")}>
            🧠 Disease Monitor Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}
