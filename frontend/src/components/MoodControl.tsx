import { useDashboard } from "../state/store";

export default function MoodControl() {
  const { state } = useDashboard();
  if (!state) return null;

  return (
    <div>
      <h2 className="font-semibold">Mood</h2>
      <p>Current: {state.mood?.mood}</p>
    </div>
  );
}
