"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BarChart3,
  Bot,
  Briefcase,
  ChevronRight,
  FileText,
  LayoutDashboard,
  LineChart,
  Shield,
  Sparkles,
  TrendingUp,
} from "lucide-react";
import clsx from "clsx";

const sections = [
  {
    label: "Overview",
    items: [{ href: "/", label: "Executive Dashboard", icon: LayoutDashboard, exact: true }],
  },
  {
    label: "Analysis",
    items: [
      { href: "/company/AAPL", label: "Company Analysis", icon: BarChart3 },
      { href: "/forecast", label: "Forecasting", icon: LineChart },
      { href: "/risk", label: "Risk Models", icon: Shield },
      { href: "/sentiment", label: "News Sentiment", icon: TrendingUp },
    ],
  },
  {
    label: "Intelligence",
    items: [
      { href: "/reports", label: "Annual Reports", icon: FileText },
      { href: "/advisor", label: "AI Advisor", icon: Bot },
      { href: "/portfolio", label: "Portfolio", icon: Briefcase },
    ],
  },
];

export function Sidebar() {
  const pathname = usePathname();

  const isActive = (href: string, exact?: boolean) =>
    exact ? pathname === href : pathname === href || pathname.startsWith(href + "/");

  return (
    <aside className="sticky top-0 flex h-screen w-[260px] shrink-0 flex-col border-r border-surface-border bg-surface-elevated/95 backdrop-blur-xl">
      <div className="border-b border-surface-border px-5 py-6">
        <Link href="/" className="group flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-accent-muted shadow-glow">
            <Sparkles className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="text-[15px] font-bold tracking-tight text-white">Financial Copilot</h1>
            <p className="text-[11px] font-medium text-slate-500">AI Investment Platform</p>
          </div>
        </Link>
      </div>

      <nav className="flex-1 space-y-6 overflow-y-auto px-3 py-5">
        {sections.map((section) => (
          <div key={section.label}>
            <p className="section-label mb-2 px-3">{section.label}</p>
            <ul className="space-y-0.5">
              {section.items.map((item) => {
                const { href, label, icon: Icon } = item;
                const exact = "exact" in item ? item.exact : false;
                const active = isActive(href, exact);
                return (
                  <li key={href}>
                    <Link
                      href={href}
                      className={clsx(
                        "group flex items-center gap-3 rounded-xl px-3 py-2.5 text-[13px] font-medium transition-all",
                        active
                          ? "bg-brand-500/10 text-brand-400 shadow-sm ring-1 ring-brand-500/20"
                          : "text-slate-400 hover:bg-surface-hover hover:text-slate-200",
                      )}
                    >
                      <Icon className={clsx("h-4 w-4 shrink-0", active && "text-brand-400")} />
                      <span className="flex-1">{label}</span>
                      {active && <ChevronRight className="h-3.5 w-3.5 opacity-60" />}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </nav>

      <div className="border-t border-surface-border p-4">
        <div className="rounded-xl border border-surface-border bg-surface-card/50 p-3">
          <p className="text-xs font-medium text-slate-300">Enterprise Edition</p>
          <p className="mt-0.5 text-[11px] text-slate-500">12 modules · Claude AI</p>
        </div>
      </div>
    </aside>
  );
}
