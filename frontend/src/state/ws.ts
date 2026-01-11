import { useEffect } from "react";
import { useDashboard } from "./store";

export function useDashboardWS() {
  const { setState } = useDashboard();

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/dashboard");

    ws.onmessage = ev => {
      const msg = JSON.parse(ev.data);

      if (msg.type === "init") {
        setState(msg.state);
      }

      if (msg.type === "engine.switch") {
        setState((s: any) => ({ ...s, active_engine: msg.engine }));
      }

      if (msg.type === "mood.update") {
        setState((s: any) => ({ ...s, mood: { mood: msg.mood } }));
      }

      if (msg.type === "plugin.loaded") {
        setState((s: any) => ({ ...s, plugins: [...s.plugins, msg.plugin] }));
      }

      if (msg.type === "plugin.unloaded") {
        setState((s: any) => ({
          ...s,
          plugins: s.plugins.filter((p: string) => p !== msg.plugin),
        }));
      }

      if (msg.type === "monitoring.update") {
        setState((s: any) => ({ ...s, ...msg }));
      }
    };

    return () => ws.close();
  }, []);
}
