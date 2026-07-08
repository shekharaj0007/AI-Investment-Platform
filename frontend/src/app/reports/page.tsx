"use client";

import { useState } from "react";
import { Loader2, PieChart, Upload } from "lucide-react";
import { uploadReport, api, ReportAnswer } from "@/lib/api";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardHeader } from "@/components/ui/Card";
import { ErrorBanner } from "@/components/ui/LoadingState";

export default function ReportsPage() {
  const [symbol, setSymbol] = useState("TSLA");
  const [file, setFile] = useState<File | null>(null);
  const [reportId, setReportId] = useState<number | null>(null);
  const [fields, setFields] = useState<Record<string, string>>({});
  const [question, setQuestion] = useState("Why did gross margin fall?");
  const [answer, setAnswer] = useState<ReportAnswer | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleUpload(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const res = await uploadReport(file, symbol);
      setReportId(res.report_id);
      setFields(res.extracted_fields);
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  async function handleAsk(e: React.FormEvent) {
    e.preventDefault();
    if (!reportId) return;
    setLoading(true);
    try {
      setAnswer(await api.askReport(reportId, question));
    } catch (err) {
      setError(String(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-6 md:p-8">
      <PageHeader
        badge="Module 2"
        title="Annual Report Reader"
        description="Upload 10-K / annual reports, extract key metrics, and ask Claude AI questions via RAG."
      />

      <div className="grid grid-cols-1 gap-8 xl:grid-cols-2">
        <Card>
          <CardHeader title="Upload Report" subtitle="PDF parsing & field extraction" />
          <form onSubmit={handleUpload} className="space-y-4">
            <div>
              <label className="section-label mb-2 block">Company Symbol</label>
              <input value={symbol} onChange={(e) => setSymbol(e.target.value.toUpperCase())} className="input-field font-mono uppercase" />
            </div>
            <div>
              <label className="section-label mb-2 block">PDF Document</label>
              <label className="flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-surface-border-light bg-surface-elevated/50 px-6 py-10 transition-colors hover:border-brand-500/40 hover:bg-surface-hover">
                <Upload className="mb-3 h-8 w-8 text-slate-500" />
                <span className="text-sm font-medium text-slate-300">{file ? file.name : "Drop PDF or click to browse"}</span>
                <input type="file" accept=".pdf" className="hidden" onChange={(e) => setFile(e.target.files?.[0] || null)} />
              </label>
            </div>
            <button type="submit" disabled={loading || !file} className="btn-primary w-full">
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Extract & Index"}
            </button>
          </form>
        </Card>

        <Card>
          <CardHeader title="Ask the Report" subtitle="RAG-powered Q&A" />
          {reportId ? (
            <form onSubmit={handleAsk} className="space-y-4">
              <textarea value={question} onChange={(e) => setQuestion(e.target.value)} rows={3} className="input-field resize-none" />
              <button type="submit" disabled={loading} className="btn-secondary w-full">Ask Claude</button>
            </form>
          ) : (
            <p className="py-8 text-center text-sm text-slate-500">Upload a report first to enable Q&A.</p>
          )}
          {answer && (
            <div className="mt-6 rounded-xl border border-surface-border bg-surface-elevated/50 p-4">
              <p className="text-sm leading-relaxed text-slate-300">{answer.answer}</p>
              {answer.sources.length > 0 && (
                <p className="mt-3 text-[11px] text-slate-600">Sources: {answer.sources.join(", ")}</p>
              )}
            </div>
          )}
        </Card>
      </div>

      {error && <div className="mt-6"><ErrorBanner message={error} /></div>}

      {Object.keys(fields).length > 0 && (
        <div className="mt-8 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {Object.entries(fields).map(([k, v]) => (
            <Card key={k} padding>
              <p className="section-label">{k}</p>
              <p className="mt-2 text-sm leading-relaxed text-slate-300">{v.slice(0, 300)}</p>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
