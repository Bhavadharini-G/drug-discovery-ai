import { useState, useEffect } from "react";
import LandingPage from "./pages/LandingPage";
import DrugDiscovery from "./components/DrugDiscovery";
import DiseaseMonitor from "./components/DiseaseMonitor";
import Sidebar from "./components/Sidebar";
import "./styles/app.css";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [page, setPage] = useState(null);
  const [showAdmin, setShowAdmin] = useState(false);
  const [history, setHistory] = useState([]);
  const [mongoStatus, setMongoStatus] = useState("checking");

  // ================= ADMIN HISTORY =================
  useEffect(() => {
    if (showAdmin) {
      fetch(`${API_BASE}/admin/history`)
        .then((res) => res.json())
        .then((data) => setHistory(data))
        .catch(() => setHistory([]));
    }
  }, [showAdmin]);

  // ================= MONGODB STATUS =================
  useEffect(() => {
    fetch(`${API_BASE}/admin/history?limit=1`)
      .then((res) => {
        if (res.ok) setMongoStatus("connected");
        else setMongoStatus("disconnected");
      })
      .catch(() => setMongoStatus("disconnected"));
  }, []);

  return (
    <div className="app-container">
      {/* ========== SIDEBAR ========== */}
      <Sidebar
        setTab={(tab) => {
          if (tab === "admin") {
            setShowAdmin(true);
            setPage(null);
          } else {
            setShowAdmin(false);
            setPage(tab);
          }
        }}
        activeTab={showAdmin ? "admin" : page}
      />

      {/* ========== MAIN CONTENT ========== */}
      <main className="main-content">
        {/* ===== SINGLE HEADER (CENTER ONLY) ===== */}
        <div className="header">
          <h1>🧬 Drug Discovery AI</h1>
          <p className="subtitle">
            AI-powered biomedical intelligence platform
          </p>

          <div className="header-status">
            {mongoStatus === "connected" && "✅ MongoDB connected"}
            {mongoStatus === "checking" && "⏳ Checking MongoDB"}
            {mongoStatus === "disconnected" && "❌ MongoDB not connected"}
          </div>
        </div>

        {/* ===== ADMIN HISTORY (CENTER) ===== */}
        {showAdmin && (
          <div className="page">
            <div className="result-box">
              <h3>🔐 Admin History</h3>

              {history.length === 0 && <p>No history records found.</p>}

              {history.map((item, idx) => (
                <details key={idx} className="admin-item">
                  <summary>
                    {item.query} — {item.query_type}
                  </summary>
                  <pre>{JSON.stringify(item.result, null, 2)}</pre>
                </details>
              ))}
            </div>
          </div>
        )}

        {/* ===== ROUTING ===== */}
        {!showAdmin && !page && <LandingPage onSelect={setPage} />}
        {!showAdmin && page === "discovery" && <DrugDiscovery />}
        {!showAdmin && page === "monitor" && <DiseaseMonitor />}
      </main>
    </div>
  );
}
