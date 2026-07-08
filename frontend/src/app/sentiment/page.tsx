"use client";

import { useEffect, useState } from "react";
import { api, SentimentScore } from "@/lib/api";
import { SentimentTimeline } from "@/components/charts/Charts";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/ui/Card";
import { StatCard } from "@/components/ui/StatCard";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/ui/LoadingState";

export default function SentimentPage() {
  const [symbol, setSymbol] = useState("TSLA");
  const [data, setData] = useState<SentimentScore | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.sentiment(symbol).then(setData).finally(() => setLoading(false));
  }, [symbol]);

  const sentimentVariant = data?.label === "Positive" ? "positive" : data?.label === "Negative" ? "negative" : "hold";

  return (
    <div className="p-6 md:p-8">
      <PageHeader
        badge="Module 8"
        title="News Sentiment"
        description="Financial lexicon analysis of news headlines with price correlation tracking."
        actions={
          <input value={symbol} onChange={(e) => setSymbol(e.target.value.toUpperCase())} className="input-field w-32 font-mono uppercase" />
        }
      />

      {loading && <LoadingState />}

      {data && !loading && (
        <>
          <div className="mb-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
            <StatCard title="Overall Sentiment" value={data.label} changeType={sentimentVariant === "positive" ? "positive" : "neutral"} highlight />
            <StatCard title="Score" value={String(data.score)} />
            <StatCard title="Articles" value={String(data.article_count)} />
            <StatCard title="Price Correlation" value={data.correlation_with_price?.toFixed(2) ?? "N/A"} />
          </div>

          <div className="mb-8">
            <SentimentTimeline timeline={data.timeline} />
          </div>

          <Card>
            <h3 className="mb-4 text-sm font-semibold text-white">Recent Headlines</h3>
            <div className="space-y-2">
              {data.articles.slice(0, 12).map((a, i) => (
                <div key={i} className="flex items-center justify-between gap-4 rounded-xl border border-surface-border/50 bg-surface-elevated/30 px-4 py-3 transition-colors hover:bg-surface-hover">
                  <span className="flex-1 text-sm text-slate-300">{a.title}</span>
                  <Badge variant={a.label === "Positive" ? "positive" : a.label === "Negative" ? "negative" : "neutral"} size="sm">
                    {a.label}
                  </Badge>
                </div>
              ))}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
