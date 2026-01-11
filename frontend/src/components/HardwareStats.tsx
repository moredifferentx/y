import { useDashboard } from "../state/store";

export default function HardwareStats() {
  const { state } = useDashboard();
  if (!state?.hardware) return null;

  return (
    <div>
      <h2 className="font-semibold">Hardware</h2>
      <p>CPU: {state.hardware.cpu_percent}%</p>
      <p>RAM: {state.hardware.memory.percent}%</p>
    </div>
  );
}
