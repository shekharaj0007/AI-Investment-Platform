"use client";

import { useEffect, useState } from "react";
import { api, ForecastResult } from "@/lib/api";
import { ForecastChart } from "@/components/charts/Charts";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/ui/Card";
import { StatCard } from "@/components/ui/StatCard";
import { LoadingState } from "@/components/ui/LoadingState";

export default function ForecastPage() {
  const [symbol, setSymbol] = useState("AAPL");
  const [metric, setMetric] = useState("revenue");
  const [model, setModel] = useState("xgboost");
  const [data, setData] = useState<ForecastResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.forecast(symbol, metric, model).then(setData).finally(() => setLoading(false));
  }, [symbol, metric, model]);

  return (
    <div className="p-6 md:p-8">
      <PageHeader
        badge="Module 4"
        title="Revenue Forecasting"
        description="ML-powered predictions using XGBoost, LightGBM, and gradient boosting with RMSE, MAE, and MAPE evaluation."
        actions={
          <div className="flex flex-wrap gap-2">
            <input value={symbol} onChange={(e) => setSymbol(e.target.value.toUpperCase())} className="input-field w-28 font-mono uppercase" />
            <select value={metric} onChange={(e) => setMetric(e.target.value)} className="input-field w-auto">
              <option value="revenue">Revenue</option>
              <option value="net_income">Net Income</option>
              <option value="eps">EPS</option>
            </select>
            <select value={model} onChange={(e) => setModel(e.target.value)} className="input-field w-auto">
              <option value="xgboost">XGBoost</option>
              <option value="lightgbm">LightGBM</option>
              <option value="gradient_boosting">Sklearn GBM</option>
            </select>
          </div>
        }
      />

      {loading && <LoadingState message="Training forecast model…" />}

      {data && !loading && (
        <>
          <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <StatCard title="RMSE" value={data.metrics.RMSE?.toLocaleString() ?? "—"} subtitle="Root mean squared error" />
            <StatCard title="MAE" value={data.metrics.MAE?.toLocaleString() ?? "—"} subtitle="Mean absolute error" />
            <StatCard title="MAPE" value={`${data.metrics.MAPE?.toFixed(1) ?? "—"}%`} subtitle={`Model: ${data.model}`} />
          </div>
          <ForecastChart historical={data.historical} forecasts={data.forecasts} />
        </>
      )}
    </div>
  );
}
