import { useDashboard } from "../state/store";

export default function EngineSwitcher() {
  const { state } = useDashboard();
  if (!state) return null;

  return (
    <div>
      <h2 className="font-semibold">AI Engines</h2>
      {state.engines.map(e => (
        <button key={e} className="mr-2 px-3 py-1 bg-blue-600 rounded">
          {e}
        </button>
      ))}
    </div>
  );
}
