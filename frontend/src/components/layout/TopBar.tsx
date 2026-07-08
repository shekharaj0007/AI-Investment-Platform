"use client";

import { useEffect, useState } from "react";
import { Activity, Circle } from "lucide-react";
import { api } from "@/lib/api";

export function TopBar() {
  const [health, setHealth] = useState<"healthy" | "offline" | "checking">("checking");

  useEffect(() => {
    api.health()
      .then((h) => setHealth(h.status === "healthy" ? "healthy" : "offline"))
      .catch(() => setHealth("offline"));
    const id = setInterval(() => {
      api.health()
        .then((h) => setHealth(h.status === "healthy" ? "healthy" : "offline"))
        .catch(() => setHealth("offline"));
    }, 30000);
    return () => clearInterval(id);
  }, []);

  return (
    <header className="sticky top-0 z-30 flex h-14 items-center justify-between border-b border-surface-border bg-surface-elevated/80 px-6 backdrop-blur-xl">
      <div className="flex items-center gap-2 text-sm text-slate-500">
        <Activity className="h-4 w-4" />
        <span>Real-time financial intelligence</span>
      </div>
      <div className="flex items-center gap-4">
        <div className="hidden items-center gap-2 text-xs text-slate-500 md:flex">
          <span className="rounded-md bg-surface-card px-2 py-1 font-mono">API :8001</span>
          <span className="rounded-md bg-surface-card px-2 py-1 font-mono">UI :3001</span>
        </div>
        <div
          className={`flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium ${
            health === "healthy"
              ? "border-brand-500/30 bg-brand-500/10 text-brand-400"
              : health === "checking"
                ? "border-amber-500/30 bg-amber-500/10 text-amber-400"
                : "border-red-500/30 bg-red-500/10 text-red-400"
          }`}
        >
          <Circle className={`h-2 w-2 fill-current ${health === "healthy" ? "animate-pulse" : ""}`} />
          {health === "healthy" ? "Systems Online" : health === "checking" ? "Connecting…" : "API Offline"}
        </div>
      </div>
    </header>
  );
}
