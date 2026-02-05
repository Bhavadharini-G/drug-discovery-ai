export default function Sidebar({ setTab, activeTab }) {
  return (
    <aside className="sidebar">
      <h3 className="sidebar-title">🧬 Modules</h3>

      <button
        className={activeTab === "discovery" ? "active" : ""}
        onClick={() => setTab("discovery")}
      >
        🧪 Drug Discovery Assistant
      </button>

      <button
        className={activeTab === "monitor" ? "active" : ""}
        onClick={() => setTab("monitor")}
      >
        🧠 Disease Monitor Dashboard
      </button>

      <button
        className={activeTab === "admin" ? "active" : ""}
        onClick={() => setTab("admin")}
      >
        🔐 Admin History
      </button>
    </aside>
  );
}
