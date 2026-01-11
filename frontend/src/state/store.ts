import { createContext, useContext, useState } from "react";

export type DashboardState = {
  engines: string[];
  active_engine: string | null;
  cloud: {
    openai: boolean;
    gemini: boolean;
  };
  personality: Record<string, number>;
  mood: {
    mood: string;
    intensity?: number;
  };
  plugins: string[];
  hardware?: any;
  metrics?: any;
  logs?: string[];
};

const DashboardContext = createContext<any>(null);

export function DashboardProvider({ children }: { children: any }) {
  const [state, setState] = useState<DashboardState | null>(null);
  return (
    <DashboardContext.Provider value={{ state, setState }}>
      {children}
    </DashboardContext.Provider>
  );
}

export function useDashboard() {
  return useContext(DashboardContext);
}
