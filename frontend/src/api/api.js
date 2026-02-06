// ================================
// API BASE URL (ENV-BASED)
// ================================
const API_BASE = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE) {
  console.error("❌ VITE_API_BASE_URL is not defined");
}

// ================= DISEASE MONITOR =================
export const runDiseaseMonitor = async (disease) => {
  const res = await fetch(
    `${API_BASE}/disease_monitor?disease=${encodeURIComponent(disease)}`
  );

  if (!res.ok) throw new Error("FastAPI error — check backend");
  return res.json();
};

// ================= FULL WORKFLOW =================
export const runFullWorkflow = async (query) => {
  const res = await fetch(
    `${API_BASE}/full_workflow?query=${encodeURIComponent(query)}`
  );

  if (!res.ok) throw new Error("FastAPI error — check backend");
  return res.json();
};

// ================= ADMIN HISTORY =================
export const fetchHistory = async (limit = 20) => {
  const res = await fetch(`${API_BASE}/admin/history?limit=${limit}`);

  if (!res.ok) throw new Error("Admin history fetch failed");
  return res.json();
};

// ================= ALPHAFOLD =================
export const fetchAlphaFold = async (gene) => {
  const res = await fetch(
    `${API_BASE}/alphafold/${encodeURIComponent(gene)}`
  );

  if (!res.ok) throw new Error("AlphaFold error");
  return res.json();
};

// ================= ADMET =================
export const runADMET = async (compound) => {
  const res = await fetch(`${API_BASE}/admet`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ compound }),
  });

  if (!res.ok) throw new Error("ADMET error");
  return res.json();
};

// ================= PATHWAY ENRICHMENT =================
export const runPathways = async (genes) => {
  const res = await fetch(`${API_BASE}/pathways`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ genes }),
  });

  if (!res.ok) throw new Error("Pathway enrichment error");
  return res.json();
};

// ================= CLINICAL TRIALS =================
export const fetchClinicalTrials = async (query) => {
  const res = await fetch(
    `${API_BASE}/clinical_trials?query=${encodeURIComponent(query)}`
  );

  if (!res.ok) throw new Error("Clinical trials error");
  return res.json();
};

// ================= BACKEND HEALTH =================
export const checkBackendHealth = async () => {
  const res = await fetch(`${API_BASE}/admin/history?limit=1`);
  return res.ok;
};
