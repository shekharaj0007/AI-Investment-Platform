"use client";

import { useState } from "react";
import { api, PortfolioResult, DCFResult } from "@/lib/api";
import { FrontierChart } from "@/components/charts/Charts";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardHeader } from "@/components/ui/Card";
import { StatCard } from "@/components/ui/StatCard";
import { Badge } from "@/components/ui/Badge";

export default function PortfolioPage() {
  const [amount, setAmount] = useState(1_000_000);
  const [risk, setRisk] = useState<"conservative" | "moderate" | "aggressive">("moderate");
  const [result, setResult] = useState<PortfolioResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [valSymbol, setValSymbol] = useState("AAPL");
  const [dcf, setDcf] = useState<DCFResult | null>(null);

  async function optimize() {
    setLoading(true);
    try {
      setResult(await api.optimizePortfolio({ total_value: amount, risk_profile: risk, currency: "INR" }));
    } finally {
      setLoading(false);
    }
  }

  async function runDcf() {
    setDcf(await api.dcf({ symbol: valSymbol, revenue_growth: 0.08, wacc: 0.10, terminal_growth: 0.03 }));
  }

  return (
    <div className="p-6 md:p-8">
      <PageHeader
        badge="Modules 7 & 9"
        title="Portfolio & Valuation"
        description="Modern Portfolio Theory optimization with efficient frontier and discounted cash flow valuation."
      />

      <div className="mb-8 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Card>
          <CardHeader title="Portfolio Optimizer" subtitle="Sharpe ratio maximization" />
          <div className="space-y-4">
            <div>
              <label className="section-label mb-2 block">Investment (₹)</label>
              <input type="number" value={amount} onChange={(e) => setAmount(Number(e.target.value))} className="input-field font-mono" />
            </div>
            <div>
              <label className="section-label mb-2 block">Risk Profile</label>
              <select value={risk} onChange={(e) => setRisk(e.target.value as typeof risk)} className="input-field">
                <option value="conservative">Conservative</option>
                <option value="moderate">Moderate</option>
                <option value="aggressive">Aggressive</option>
              </select>
            </div>
            <button onClick={optimize} disabled={loading} className="btn-primary w-full">
              {loading ? "Optimizing…" : "Optimize Portfolio"}
            </button>
          </div>
        </Card>

        <Card>
          <CardHeader title="DCF Valuation" subtitle="Discounted cash flow model" />
          <div className="flex gap-2">
            <input value={valSymbol} onChange={(e) => setValSymbol(e.target.value.toUpperCase())} className="input-field flex-1 font-mono uppercase" />
            <button onClick={runDcf} className="btn-secondary shrink-0">Run DCF</button>
          </div>
          {dcf && (
            <div className="mt-6 space-y-3 rounded-xl bg-surface-elevated/50 p-4">
              <div className="flex justify-between text-sm"><span className="text-slate-500">Enterprise Value</span><span className="font-mono text-white">${dcf.enterprise_value.toLocaleString()}</span></div>
              <div className="flex justify-between text-sm"><span className="text-slate-500">Equity Value</span><span className="font-mono text-white">${dcf.equity_value.toLocaleString()}</span></div>
              <div className="flex justify-between border-t border-surface-border pt-3 text-sm"><span className="text-slate-500">Fair Price</span><span className="font-mono text-lg font-semibold text-brand-400">${dcf.fair_share_price.toFixed(2)}</span></div>
            </div>
          )}
        </Card>
      </div>

      {result && (
        <>
          <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <StatCard title="Expected Return" value={`${(result.expected_return * 100).toFixed(1)}%`} changeType="positive" highlight />
            <StatCard title="Volatility" value={`${(result.volatility * 100).toFixed(1)}%`} />
            <StatCard title="Sharpe Ratio" value={result.sharpe_ratio.toFixed(2)} subtitle={result.risk_profile} />
          </div>

          <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
            <Card>
              <CardHeader title="Asset Allocation" subtitle={`Total ₹${result.total_value.toLocaleString("en-IN")}`} />
              <div className="space-y-2">
                {result.allocations.map((a) => (
                  <div key={a.symbol} className="flex items-center gap-4">
                    <div className="flex-1">
                      <div className="flex justify-between text-sm">
                        <span className="font-medium text-white">{a.asset_class} <span className="text-slate-500">{a.symbol}</span></span>
                        <span className="font-mono text-brand-400">{(a.weight * 100).toFixed(0)}%</span>
                      </div>
                      <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-surface-elevated">
                        <div className="h-full rounded-full bg-gradient-to-r from-brand-600 to-brand-400" style={{ width: `${a.weight * 100}%` }} />
                      </div>
                    </div>
                    <span className="shrink-0 font-mono text-xs text-slate-500">₹{a.amount.toLocaleString("en-IN")}</span>
                  </div>
                ))}
              </div>
            </Card>
            {result.efficient_frontier.length > 0 && <FrontierChart frontier={result.efficient_frontier} />}
          </div>
        </>
      )}

      {dcf && dcf.comparables.length > 0 && (
        <div className="mt-8">
          <p className="section-label mb-4">Comparable Companies</p>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            {dcf.comparables.map((c) => (
              <Card key={c.symbol}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-white">{c.symbol}</p>
                    <p className="text-xs text-slate-500">{c.name}</p>
                  </div>
                  <Badge variant="info">P/E {c.pe_ratio?.toFixed(1) ?? "—"}</Badge>
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
