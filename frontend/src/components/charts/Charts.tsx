"use client";

import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Card, CardHeader } from "@/components/ui/Card";

type Point = { period: string; value: number };

const tooltipStyle = {
  background: "rgba(17, 24, 39, 0.95)",
  border: "1px solid #334155",
  borderRadius: 12,
  boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
  fontSize: 12,
};

export function TrendChart({
  data,
  title,
  subtitle,
  color = "#10b981",
  formatValue,
}: {
  data: Point[];
  title: string;
  subtitle?: string;
  color?: string;
  formatValue?: (v: number) => string;
}) {
  const fmt = formatValue || ((v: number) => v.toLocaleString());
  const gradId = `grad-${title.replace(/\s/g, "")}`;

  return (
    <Card>
      <CardHeader title={title} subtitle={subtitle} />
      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={data} margin={{ top: 4, right: 4, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id={gradId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={color} stopOpacity={0.25} />
              <stop offset="100%" stopColor={color} stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke="#1e293b" strokeDasharray="4 4" vertical={false} />
          <XAxis dataKey="period" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
          <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} tickFormatter={(v) => fmt(v)} />
          <Tooltip contentStyle={tooltipStyle} formatter={(v: number) => [fmt(v), "Value"]} />
          <Area type="monotone" dataKey="value" stroke={color} fill={`url(#${gradId})`} strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </Card>
  );
}

export function DualTrendChart({ revenue, profit }: { revenue: Point[]; profit: Point[] }) {
  const merged = revenue.map((r, i) => ({
    period: r.period?.slice(0, 7) || r.period,
    revenue: r.value,
    profit: profit[i]?.value ?? 0,
  }));

  return (
    <Card>
      <CardHeader title="Revenue & Profit" subtitle="Historical performance trends" />
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={merged} margin={{ top: 4, right: 4, left: 0, bottom: 0 }}>
          <CartesianGrid stroke="#1e293b" strokeDasharray="4 4" vertical={false} />
          <XAxis dataKey="period" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
          <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
          <Tooltip contentStyle={tooltipStyle} />
          <Legend wrapperStyle={{ fontSize: 12, paddingTop: 12 }} />
          <Line type="monotone" dataKey="revenue" name="Revenue" stroke="#10b981" strokeWidth={2.5} dot={false} />
          <Line type="monotone" dataKey="profit" name="Net Profit" stroke="#3b82f6" strokeWidth={2.5} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
}

export function ForecastChart({
  historical,
  forecasts,
}: {
  historical: Array<{ period: string; value: number }>;
  forecasts: Array<{ period: string; value: number; lower_bound?: number; upper_bound?: number }>;
}) {
  const data = [
    ...historical.map((h) => ({ period: h.period, actual: h.value, forecast: null as number | null })),
    ...forecasts.map((f) => ({ period: f.period, actual: null as number | null, forecast: f.value })),
  ];

  return (
    <Card>
      <CardHeader title="Forecast Model" subtitle="Historical actuals vs projected values" />
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 4, right: 4, left: 0, bottom: 0 }}>
          <CartesianGrid stroke="#1e293b" strokeDasharray="4 4" vertical={false} />
          <XAxis dataKey="period" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
          <YAxis stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} />
          <Tooltip contentStyle={tooltipStyle} />
          <Legend wrapperStyle={{ fontSize: 12, paddingTop: 12 }} />
          <Line type="monotone" dataKey="actual" name="Actual" stroke="#10b981" strokeWidth={2.5} connectNulls={false} dot={false} />
          <Line type="monotone" dataKey="forecast" name="Forecast" stroke="#f59e0b" strokeWidth={2.5} strokeDasharray="6 4" connectNulls={false} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
}

export function SentimentTimeline({
  timeline,
}: {
  timeline: Array<{ date: string; score: number; label: string }>;
}) {
  return (
    <Card>
      <CardHeader title="Sentiment Timeline" subtitle="News sentiment scores over time" />
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={timeline} margin={{ top: 4, right: 4, left: 0, bottom: 0 }}>
          <CartesianGrid stroke="#1e293b" strokeDasharray="4 4" vertical={false} />
          <XAxis dataKey="date" stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
          <YAxis stroke="#64748b" domain={[-1, 1]} fontSize={11} tickLine={false} axisLine={false} />
          <Tooltip contentStyle={tooltipStyle} />
          <Bar dataKey="score" fill="#10b981" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}

export function FrontierChart({
  frontier,
}: {
  frontier: Array<{ volatility: number; expected_return: number }>;
}) {
  return (
    <Card>
      <CardHeader title="Efficient Frontier" subtitle="Risk-return optimization curve" />
      <ResponsiveContainer width="100%" height={260}>
        <LineChart data={frontier} margin={{ top: 4, right: 16, left: 0, bottom: 0 }}>
          <CartesianGrid stroke="#1e293b" strokeDasharray="4 4" />
          <XAxis dataKey="volatility" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
          <YAxis dataKey="expected_return" stroke="#64748b" fontSize={11} tickLine={false} axisLine={false} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
          <Tooltip contentStyle={tooltipStyle} />
          <Line type="monotone" dataKey="expected_return" stroke="#10b981" strokeWidth={2.5} dot={{ r: 4, fill: "#10b981" }} />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
}
