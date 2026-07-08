"use client";

import { useState } from "react";
import { Bot, Loader2, Sparkles } from "lucide-react";
import { api, AdvisorResponse } from "@/lib/api";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardHeader } from "@/components/ui/Card";
import { Badge, recommendationVariant } from "@/components/ui/Badge";
import { ErrorBanner } from "@/components/ui/LoadingState";

export default function AdvisorPage() {
  const [question, setQuestion] = useState("Should I buy Infosys?");
  const [symbol, setSymbol] = useState("INFY");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AdvisorResponse | null>(null);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      setResult(await api.askAdvisor({ question, symbol: symbol || undefined }));
    } catch {
      setError("Could not reach the API. Ensure the backend is running on port 8001.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-6 md:p-8">
      <PageHeader
        badge="Module 10"
        title="AI Investment Advisor"
        description="Claude-powered analysis grounded in ratios, forecasts, risk models, and news sentiment with SHAP explanations."
      />

      <div className="grid grid-cols-1 gap-8 xl:grid-cols-5">
        <Card className="xl:col-span-2">
          <CardHeader title="Ask a Question" subtitle="Powered by Claude AI" />
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="section-label mb-2 block">Ticker Symbol</label>
              <input
                value={symbol}
                onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                className="input-field font-mono uppercase"
                placeholder="INFY"
              />
            </div>
            <div>
              <label className="section-label mb-2 block">Your Question</label>
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                rows={4}
                className="input-field resize-none"
                placeholder="Should I buy this stock for long-term holding?"
              />
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full">
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" /> Analyzing…
                </>
              ) : (
                <>
                  <Bot className="h-4 w-4" /> Get Recommendation
                </>
              )}
            </button>
          </form>
        </Card>

        <div className="space-y-6 xl:col-span-3">
          {error && <ErrorBanner message={error} />}

          {!result && !loading && (
            <Card className="flex flex-col items-center justify-center py-16 text-center">
              <div className="mb-4 rounded-2xl bg-brand-500/10 p-4">
                <Sparkles className="h-8 w-8 text-brand-400" />
              </div>
              <p className="text-sm text-slate-400">Submit a question to receive an AI-powered investment analysis.</p>
            </Card>
          )}

          {result && (
            <>
              <Card>
                <div className="flex flex-wrap items-center gap-3">
                  <Badge variant={recommendationVariant(result.recommendation)} size="md">
                    {result.recommendation}
                  </Badge>
                  {result.symbol && <Badge variant="info">{result.symbol}</Badge>}
                  <span className="text-sm text-slate-500">
                    Confidence: <span className="font-mono font-medium text-slate-300">{(result.confidence * 100).toFixed(0)}%</span>
                  </span>
                </div>
                <p className="mt-5 text-[15px] leading-relaxed text-slate-300">{result.summary}</p>
              </Card>

              <Card>
                <CardHeader title="Explainable AI" subtitle="SHAP feature contributions" />
                <div className="space-y-1">
                  {result.explanations.map((exp) => (
                    <div
                      key={exp.feature}
                      className="flex items-center justify-between rounded-xl px-3 py-3 transition-colors hover:bg-surface-hover"
                    >
                      <div>
                        <p className="text-sm font-medium text-white">{exp.feature}</p>
                        <p className="text-xs text-slate-500">{exp.value}</p>
                      </div>
                      <div className="text-right">
                        <Badge
                          variant={
                            exp.impact === "Positive" || exp.impact === "Low" || exp.impact === "Improving"
                              ? "positive"
                              : exp.impact === "Negative"
                                ? "negative"
                                : "hold"
                          }
                          size="sm"
                        >
                          {exp.impact}
                        </Badge>
                        {exp.shap_value != null && (
                          <p className="mt-1 font-mono text-[10px] text-slate-600">SHAP {exp.shap_value.toFixed(2)}</p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
