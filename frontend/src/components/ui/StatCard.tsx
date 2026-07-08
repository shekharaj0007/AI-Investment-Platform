import clsx from "clsx";
import { LucideIcon, TrendingDown, TrendingUp, Minus } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string;
  subtitle?: string;
  change?: string;
  changeType?: "positive" | "negative" | "neutral";
  icon?: LucideIcon;
  highlight?: boolean;
}

export function StatCard({
  title,
  value,
  subtitle,
  change,
  changeType = "neutral",
  icon: Icon,
  highlight,
}: StatCardProps) {
  const TrendIcon =
    changeType === "positive" ? TrendingUp : changeType === "negative" ? TrendingDown : Minus;

  return (
    <div
      className={clsx(
        "glass-card group relative overflow-hidden p-5 transition-all hover:border-surface-border-light",
        highlight && "ring-1 ring-brand-500/20",
      )}
    >
      {highlight && (
        <div className="pointer-events-none absolute -right-8 -top-8 h-24 w-24 rounded-full bg-brand-500/10 blur-2xl" />
      )}
      <div className="flex items-start justify-between gap-3">
        <p className="section-label">{title}</p>
        {Icon && (
          <div className="rounded-lg bg-surface-hover p-2 text-slate-400">
            <Icon className="h-4 w-4" />
          </div>
        )}
      </div>
      <p className="metric-value mt-3">{value}</p>
      {subtitle && <p className="mt-1 text-xs text-slate-500">{subtitle}</p>}
      {change && (
        <div
          className={clsx("mt-3 flex items-center gap-1.5 text-xs font-medium", {
            "text-emerald-400": changeType === "positive",
            "text-red-400": changeType === "negative",
            "text-slate-500": changeType === "neutral",
          })}
        >
          <TrendIcon className="h-3.5 w-3.5" />
          {change}
        </div>
      )}
    </div>
  );
}
