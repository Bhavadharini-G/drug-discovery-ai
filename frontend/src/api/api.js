// ================================
// API BASE URL (ENV-BASED)
// ================================
const API_BASE = import.meta.env.VITE_API_BASE_URL;

// ================= DISEASE MONITOR =================
export const runDiseaseMonitor = async (disease) => {
  const res = await fetch(
    `${API_URL}/disease_monitor?disease=${encodeURIComponent(disease)}`
  );
  return res.json();
};

// ================= FULL WORKFLOW =================
export const runFullWorkflow = async (query) => {
  const res = await fetch(
    `${API_URL}/full_workflow?query=${encodeURIComponent(query)}`
  );
  return res.json();
};

// ================= ADMIN HISTORY =================
export const fetchHistory = async () => {
  const res = await fetch(`${API_URL}/admin/history`);
  return res.json();
};

/* ==================================================
   ENGINE APIs
   ================================================== */

// ================= ALPHAFOLD =================
export const fetchAlphaFold = async (gene) => {
  const res = await fetch(
    `${API_URL}/alphafold/${encodeURIComponent(gene)}`
  );
  return res.json();
};

// ================= ADMET =================
export const runADMET = async (compound) => {
  const res = await fetch(`${API_URL}/admet`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ compound }),
  });
  return res.json();
};

// ================= PATHWAY ENRICHMENT =================
export const runPathways = async (genes) => {
  const res = await fetch(`${API_URL}/pathways`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ genes }),
  });
  return res.json();
};

// ================= CLINICAL TRIALS =================
export const fetchClinicalTrials = async (query) => {
  const res = await fetch(
    `${API_URL}/clinical_trials?query=${encodeURIComponent(query)}`
  );
  return res.json();
};
