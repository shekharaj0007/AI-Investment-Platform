"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const data = [
  { quarter: "Q1 24", revenue: 94.8, profit: 23.6 },
  { quarter: "Q2 24", revenue: 97.2, profit: 24.1 },
  { quarter: "Q3 24", revenue: 101.5, profit: 25.8 },
  { quarter: "Q4 24", revenue: 105.3, profit: 27.2 },
  { quarter: "Q1 25", revenue: 109.1, profit: 28.5 },
  { quarter: "Q2 25", revenue: 113.4, profit: 29.9 },
];

export function RevenueChart() {
  return (
    <div className="rounded-xl border border-surface-border bg-surface-card p-5">
      <h3 className="mb-4 text-sm font-medium text-slate-300">Revenue & Profit Trends</h3>
      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="quarter" stroke="#94a3b8" fontSize={12} />
          <YAxis stroke="#94a3b8" fontSize={12} />
          <Tooltip
            contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }}
          />
          <Area
            type="monotone"
            dataKey="revenue"
            stroke="#22c55e"
            fill="url(#revenueGrad)"
            strokeWidth={2}
          />
          <Area type="monotone" dataKey="profit" stroke="#3b82f6" fill="none" strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
