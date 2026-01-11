import React from "react";
import ReactDOM from "react-dom/client";
import App from "./app";
import { DashboardProvider } from "./state/store";
import "./styles/theme.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <DashboardProvider>
      <App />
    </DashboardProvider>
  </React.StrictMode>
);
