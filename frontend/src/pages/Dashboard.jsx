import DiseaseDiscovery from "../components/DiseaseDiscovery";
import DiseaseMonitor from "../components/DiseaseMonitor";

export default function Dashboard({ module }) {
  return (
    <div className="dashboard">
      {module === "drug" && <DiseaseDiscovery />}
      {module === "monitor" && <DiseaseMonitor />}
    </div>
  );
}
