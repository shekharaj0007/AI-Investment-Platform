"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Building2, DollarSign } from "lucide-react";
import { api, CompanyFinancials, CompanyProfile, RatioAnalysis } from "@/lib/api";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardHeader } from "@/components/ui/Card";
import { StatCard } from "@/components/ui/StatCard";
import { DualTrendChart } from "@/components/charts/Charts";
import { ErrorBanner, LoadingState } from "@/components/ui/LoadingState";
import { Badge } from "@/components/ui/Badge";

export default function CompanyPage() {
  const params = useParams();
  const symbol = (params.symbol as string)?.toUpperCase() || "AAPL";
  const [profile, setProfile] = useState<CompanyProfile | null>(null);
  const [financials, setFinancials] = useState<CompanyFinancials | null>(null);
  const [ratios, setRatios] = useState<RatioAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    Promise.all([api.company(symbol), api.financials(symbol), api.ratios(symbol)])
      .then(([p, f, r]) => { setProfile(p); setFinancials(f); setRatios(r); })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [symbol]);

  const revenue = financials?.income_statements.map((s) => ({ period: s.period.slice(0, 7), value: s.revenue || 0 })).reverse() || [];
  const profit = financials?.income_statements.map((s) => ({ period: s.period.slice(0, 7), value: s.net_income || 0 })).reverse() || [];

  return (
    <div className="p-6 md:p-8">
      <PageHeader
        badge="Modules 1 & 3"
        title={profile?.name || symbol}
        description={[profile?.sector, profile?.industry].filter(Boolean).join(" · ") || "Company financial analysis"}
        actions={<Badge variant="info">{symbol}</Badge>}
      />

      {error && <ErrorBanner message={error} />}
      {loading && <LoadingState />}

      {profile && !loading && (
        <>
          <div className="mb-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
            <StatCard title="Share Price" value={`$${profile.current_price?.toFixed(2) ?? "—"}`} icon={DollarSign} highlight />
            <StatCard title="Market Cap" value={profile.market_cap ? `$${(profile.market_cap / 1e9).toFixed(1)}B` : "—"} icon={Building2} />
            <StatCard title="P/E Ratio" value={profile.pe_ratio?.toFixed(1) ?? "—"} />
            <StatCard title="P/B Ratio" value={profile.pb_ratio?.toFixed(1) ?? "—"} />
          </div>

          {revenue.length > 0 && (
            <div className="mb-8">
              <DualTrendChart revenue={revenue} profit={profit} />
            </div>
          )}

          {ratios && (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
              {ratios.categories.map((cat) => (
                <Card key={cat.name}>
                  <CardHeader title={cat.name} />
                  {Object.entries(cat.metrics).map(([k, v]) => (
                    <div key={k} className="flex justify-between border-b border-surface-border/50 py-2.5 text-sm last:border-0">
                      <span className="text-slate-400">{k}</span>
                      <span className="font-mono font-medium text-white">
                        {v != null ? (Math.abs(v) < 5 ? `${(v * 100).toFixed(1)}%` : v.toLocaleString()) : "—"}
                      </span>
                    </div>
                  ))}
                </Card>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
