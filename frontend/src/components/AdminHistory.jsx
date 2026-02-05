import { useEffect, useState } from "react";
import { fetchHistory } from "../api/api";

export default function AdminHistory() {
  const [rows, setRows] = useState([]);

  useEffect(() => {
    fetchHistory().then(setRows);
  }, []);

  return (
    <>
      <h1>🔐 Admin History</h1>

      {rows.map(r => (
        <details key={r._id}>
          <summary>
            {r.query} | {r.query_type} | {new Date(r.timestamp).toLocaleString()}
          </summary>
          <p>Result stored successfully.</p>
        </details>
      ))}
    </>
  );
}
