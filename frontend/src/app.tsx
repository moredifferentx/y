import { useDashboardWS } from "./state/ws";
import Dashboard from "./pages/Dashboard";

export default function App() {
  useDashboardWS();
  return <Dashboard />;
}
