import { useState, useEffect } from "react";
import LandingPage from "./pages/LandingPage";
import DrugDiscovery from "./components/DrugDiscovery";
import DiseaseMonitor from "./components/DiseaseMonitor";
import Sidebar from "./components/Sidebar";
import "./styles/App.css";

// ================================
// ENV
// ================================
const API_BASE = import.meta.env.VITE_API_BASE_URL;
const ENABLE_LOGIN = import.meta.env.VITE_ENABLE_LOGIN === "true";

export default function App() {
  const [page, setPage] = useState(null);
  const [showAdmin, setShowAdmin] = useState(false);
  const [history, setHistory] = useState([]);
  const [mongoStatus, setMongoStatus] = useState("checking");

  // ================= AUTH =================
  const [isAuthenticated, setIsAuthenticated] = useState(
    localStorage.getItem("auth") === "true"
  );

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

  // ================= LOGIN GATE =================
  if (ENABLE_LOGIN && !isAuthenticated) {
    return (
      <LandingPage
        onLoginSuccess={() => {
          localStorage.setItem("auth", "true");
          setIsAuthenticated(true);
        }}
      />
    );
  }

  // ================= MAIN APP =================
  return (
    <div className="app-container">
      {/* ===== SIDEBAR ===== */}
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

      {/* ===== MAIN CONTENT ===== */}
      <main className="main-content">
        <div className="header">
          <h1>🧬 Drug Discovery AI</h1>
          <p className="subtitle">
            AI-powered biomedical intelligence platform
          </p>

          <div className="header-status">
            {mongoStatus === "connected" && "✅ MongoDB connected"}
            {mongoStatus === "checking" && "⏳ Checking MongoDB"}
            {mongoStatus === "disconnected" && "❌ MongoDB not connected"}

            {/* ===== LOGOUT ===== */}
            <button
              style={{ marginLeft: "16px" }}
              onClick={() => {
                localStorage.removeItem("auth");
                window.location.reload();
              }}
            >
              🚪 Logout
            </button>
          </div>
        </div>

        {/* ===== ADMIN HISTORY ===== */}
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

        {/* ===== ROUTES ===== */}
        {!showAdmin && !page && <LandingPage onSelect={setPage} />}
        {!showAdmin && page === "discovery" && <DrugDiscovery />}
        {!showAdmin && page === "monitor" && <DiseaseMonitor />}
      </main>
    </div>
  );
}
