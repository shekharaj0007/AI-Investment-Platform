"use client";

import { useEffect, useState } from "react";
import { Building2, DollarSign, Shield, Sparkles, TrendingUp } from "lucide-react";
import { api, DashboardSummary } from "@/lib/api";
import { StatCard } from "@/components/ui/StatCard";
import { DualTrendChart, SentimentTimeline, TrendChart } from "@/components/charts/Charts";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge, recommendationVariant } from "@/components/ui/Badge";
import { ErrorBanner, LoadingState } from "@/components/ui/LoadingState";
import { Search } from "lucide-react";

export default function DashboardPage() {
  const [symbol, setSymbol] = useState("AAPL");
  const [input, setInput] = useState("AAPL");
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    setError("");
    api.dashboard(symbol)
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [symbol]);

  return (
    <div className="p-6 md:p-8">
      <PageHeader
        badge="Module 12"
        title="Executive Dashboard"
        description="Unified view of financial performance, risk metrics, forecasts, and AI-driven recommendations."
        actions={
          <form
            onSubmit={(e) => {
              e.preventDefault();
              setSymbol(input.toUpperCase());
            }}
            className="flex gap-2"
          >
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
              <input
                value={input}
                onChange={(e) => setInput(e.target.value.toUpperCase())}
                className="input-field w-36 pl-9 font-mono uppercase md:w-44"
                placeholder="Symbol"
              />
            </div>
            <button type="submit" className="btn-primary">
              Analyze
            </button>
          </form>
        }
      />

      {error && <ErrorBanner message={error} />}
      {loading && !data && <LoadingState message="Building executive summary…" />}

      {data && (
        <>
          <div className="mb-6 flex flex-wrap items-center gap-3">
            <h2 className="text-lg font-semibold text-white">{data.company_name}</h2>
            <Badge variant="info">{data.symbol}</Badge>
            <Badge variant={recommendationVariant(data.recommendation)}>{data.recommendation}</Badge>
          </div>

          <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <StatCard
              title="Share Price"
              value={`$${data.current_price?.toFixed(2) ?? "—"}`}
              subtitle={data.symbol}
              icon={DollarSign}
              highlight
            />
            <StatCard
              title="Market Cap"
              value={data.market_cap ? `$${(data.market_cap / 1e9).toFixed(1)}B` : "—"}
              icon={Building2}
            />
            <StatCard
              title="Bankruptcy Risk"
              value={`${data.bankruptcy_probability}%`}
              changeType={data.bankruptcy_probability < 15 ? "positive" : "negative"}
              change="ML probability"
              icon={Shield}
            />
            <StatCard
              title="Fair Value (DCF)"
              value={`$${data.fair_share_price?.toFixed(2) ?? "—"}`}
              change={data.recommendation}
              changeType={data.recommendation === "Buy" ? "positive" : "neutral"}
              icon={TrendingUp}
            />
          </div>

          <div className="mb-8 grid grid-cols-1 gap-6 xl:grid-cols-2">
            <DualTrendChart revenue={data.revenue_trend} profit={data.profit_trend} />
            <TrendChart
              data={data.cash_flow_trend}
              title="Cash Flow"
              subtitle="Operating & free cash flow"
              color="#3b82f6"
              formatValue={(v) => `$${(v / 1e9).toFixed(1)}B`}
            />
          </div>

          <div className="mb-8 grid grid-cols-1 gap-6 lg:grid-cols-3">
            <Card className="lg:col-span-1">
              <CardHeader title="Key Ratios" subtitle="Latest financial metrics" />
              <dl className="space-y-3">
                {Object.entries(data.ratio_summary).slice(0, 8).map(([k, v]) => (
                  <div key={k} className="flex items-center justify-between border-b border-surface-border/60 pb-2 last:border-0">
                    <dt className="text-sm text-slate-400">{k}</dt>
                    <dd className="font-mono text-sm font-medium text-white">
                      {typeof v === "number" ? (Math.abs(v) < 5 ? `${(v * 100).toFixed(1)}%` : v.toFixed(2)) : "—"}
                    </dd>
                  </div>
                ))}
              </dl>
            </Card>
            <div className="lg:col-span-2">
              <SentimentTimeline timeline={data.sentiment.timeline} />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <StatCard
              title="News Sentiment"
              value={data.sentiment.label}
              change={`Score ${data.sentiment.score}`}
              changeType={data.sentiment.label === "Positive" ? "positive" : "neutral"}
              icon={Sparkles}
            />
            <StatCard title="Portfolio Sharpe" value={data.portfolio_sharpe?.toFixed(2) ?? "—"} subtitle="Moderate profile" />
            <StatCard
              title="Revenue Forecast"
              value={data.forecast_summary[0] ? `$${(data.forecast_summary[0].value / 1e9).toFixed(1)}B` : "—"}
              subtitle={data.forecast_summary[0]?.period}
            />
          </div>
        </>
      )}
    </div>
  );
}
