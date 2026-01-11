import { useDashboard } from "../state/store";

export default function LogsViewer() {
  const { state } = useDashboard();
  if (!state?.logs) return null;

  return (
    <div>
      <h2 className="font-semibold">Logs</h2>
      <pre className="bg-black p-2 text-xs max-h-40 overflow-y-scroll">
        {state.logs.join("\n")}
      </pre>
    </div>
  );
}
