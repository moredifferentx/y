import { useDashboard } from "../state/store";
import EngineSwitcher from "../components/EngineSwitcher";
import MoodControl from "../components/MoodControl";
import HardwareStats from "../components/HardwareStats";
import LogsViewer from "../components/LogsViewer";

export default function Dashboard() {
  const { state } = useDashboard();
  if (!state) return <div>Loading dashboard…</div>;

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <EngineSwitcher />
      <MoodControl />
      <HardwareStats />
      <LogsViewer />
    </div>
  );
}
