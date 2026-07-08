"use client";

import { useEffect, useState } from "react";
import { api, BankruptcyRisk, CreditRisk } from "@/lib/api";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/ui/LoadingState";

export default function RiskPage() {
  const [symbol, setSymbol] = useState("AAPL");
  const [bankruptcy, setBankruptcy] = useState<BankruptcyRisk | null>(null);
  const [credit, setCredit] = useState<CreditRisk | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([api.bankruptcy(symbol), api.credit(symbol)])
      .then(([b, c]) => { setBankruptcy(b); setCredit(c); })
      .finally(() => setLoading(false));
  }, [symbol]);

  return (
    <div className="p-6 md:p-8">
      <PageHeader
        badge="Modules 5 & 6"
        title="Risk Models"
        description="Altman Z-score bankruptcy prediction, credit rating classification, and SHAP explainability."
        actions={
          <input value={symbol} onChange={(e) => setSymbol(e.target.value.toUpperCase())} className="input-field w-32 font-mono uppercase" />
        }
      />

      {loading && <LoadingState />}

      {!loading && (
        <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
          {bankruptcy && (
            <Card>
              <CardHeader title="Bankruptcy Prediction" subtitle="Altman Z-score + Random Forest" />
              <div className="mb-6 grid grid-cols-3 gap-4">
                <div className="rounded-xl bg-surface-elevated p-4 text-center">
                  <p className="section-label">Z-Score</p>
                  <p className="metric-value mt-2 text-xl">{bankruptcy.altman_z_score}</p>
                </div>
                <div className="rounded-xl bg-surface-elevated p-4 text-center">
                  <p className="section-label">Zone</p>
                  <div className="mt-2">
                    <Badge variant={bankruptcy.zone === "Safe" ? "positive" : "hold"}>{bankruptcy.zone}</Badge>
                  </div>
                </div>
                <div className="rounded-xl bg-surface-elevated p-4 text-center">
                  <p className="section-label">Probability</p>
                  <p className="metric-value mt-2 text-xl text-red-400">{bankruptcy.ml_probability}%</p>
                </div>
              </div>
              <p className="section-label mb-3">SHAP Explanations</p>
              <div className="space-y-2">
                {bankruptcy.shap_explanations.map((e) => (
                  <div key={e.feature} className="flex justify-between rounded-lg bg-surface-elevated/50 px-3 py-2 text-sm">
                    <span className="text-slate-400">{e.feature}</span>
                    <span className="font-mono text-slate-300">{e.shap_value}</span>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {credit && (
            <Card>
              <CardHeader title="Credit Risk" subtitle="Rating & default probability" />
              <div className="mb-6 flex items-center gap-6">
                <div>
                  <p className="section-label">Rating</p>
                  <p className="mt-1 text-4xl font-bold text-brand-400">{credit.predicted_rating}</p>
                </div>
                <div>
                  <p className="section-label">Default Prob.</p>
                  <p className="metric-value mt-1">{credit.default_probability}%</p>
                </div>
                <div>
                  <p className="section-label">Confidence</p>
                  <p className="metric-value mt-1">{(credit.confidence * 100).toFixed(0)}%</p>
                </div>
              </div>
              <p className="section-label mb-3">Feature Contributions</p>
              <div className="space-y-2">
                {credit.shap_explanations.map((e) => (
                  <div key={e.feature} className="flex justify-between rounded-lg bg-surface-elevated/50 px-3 py-2 text-sm">
                    <span className="text-slate-400">{e.feature}</span>
                    <span className="font-mono text-slate-300">{e.shap_value}</span>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
