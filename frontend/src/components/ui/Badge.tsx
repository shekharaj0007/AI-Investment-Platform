import clsx from "clsx";

type BadgeVariant = "buy" | "sell" | "hold" | "positive" | "negative" | "neutral" | "info";

const variants: Record<BadgeVariant, string> = {
  buy: "border-emerald-500/30 bg-emerald-500/10 text-emerald-400",
  sell: "border-red-500/30 bg-red-500/10 text-red-400",
  hold: "border-amber-500/30 bg-amber-500/10 text-amber-400",
  positive: "border-emerald-500/30 bg-emerald-500/10 text-emerald-400",
  negative: "border-red-500/30 bg-red-500/10 text-red-400",
  neutral: "border-surface-border-light bg-surface-hover text-slate-400",
  info: "border-blue-500/30 bg-blue-500/10 text-blue-400",
};

export function Badge({
  children,
  variant = "neutral",
  size = "md",
}: {
  children: React.ReactNode;
  variant?: BadgeVariant;
  size?: "sm" | "md";
}) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full border font-semibold",
        variants[variant],
        size === "sm" ? "px-2 py-0.5 text-[10px] uppercase tracking-wide" : "px-3 py-1 text-xs",
      )}
    >
      {children}
    </span>
  );
}

export function recommendationVariant(rec: string): BadgeVariant {
  if (rec === "Buy") return "buy";
  if (rec === "Sell") return "sell";
  return "hold";
}
