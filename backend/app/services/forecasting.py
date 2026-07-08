"""Module 4: Revenue Forecasting with XGBoost / sklearn fallback."""

from __future__ import annotations

import numpy as np

from app.schemas.financial import ForecastPoint, ForecastResult
from app.services.financial_data import FinancialDataService

METRIC_KEYS = {
    "revenue": "revenue",
    "net_income": "net_income",
    "eps": "eps",
    "operating_cash_flow": "operating_cash_flow",
}


class ForecastingService:
    def __init__(self) -> None:
        self._data = FinancialDataService()

    async def forecast(
        self,
        symbol: str,
        metric: str = "revenue",
        model: str = "xgboost",
        periods: int = 4,
    ) -> ForecastResult:
        financials = await self._data.get_financials(symbol)
        key = METRIC_KEYS.get(metric, "revenue")

        historical_values: list[tuple[str, float]] = []
        for stmt in reversed(financials.income_statements):
            val = getattr(stmt, key, None)
            if stmt.period and val and val > 0:
                historical_values.append((stmt.period, val))

        if len(historical_values) < 2:
            base = historical_values[0][1] if historical_values else 1_000_000.0
            forecasts = [
                ForecastPoint(period=f"FY+{i+1}", value=round(base * 1.08 ** (i + 1), 2))
                for i in range(periods)
            ]
            return ForecastResult(
                symbol=symbol.upper(),
                metric=metric,
                model="growth_stub",
                forecasts=forecasts,
                historical=[ForecastPoint(period=p, value=v) for p, v in historical_values],
                metrics={"RMSE": 0, "MAE": 0, "MAPE": 0},
            )

        values = np.array([v for _, v in historical_values], dtype=float)
        X = np.arange(len(values)).reshape(-1, 1)
        y = values

        preds, eval_metrics, used_model = _train_and_predict(X, y, periods, model)

        historical = [ForecastPoint(period=p, value=round(v, 2)) for p, v in historical_values]
        forecasts = []
        for i, pred in enumerate(preds):
            std = eval_metrics.get("std", pred * 0.1)
            forecasts.append(
                ForecastPoint(
                    period=f"FY+{i+1}",
                    value=round(float(pred), 2),
                    lower_bound=round(float(pred - 1.28 * std), 2),
                    upper_bound=round(float(pred + 1.28 * std), 2),
                )
            )

        return ForecastResult(
            symbol=symbol.upper(),
            metric=metric,
            model=used_model,
            forecasts=forecasts,
            historical=historical,
            metrics={
                "RMSE": round(eval_metrics.get("rmse", 0), 2),
                "MAE": round(eval_metrics.get("mae", 0), 2),
                "MAPE": round(eval_metrics.get("mape", 0), 2),
            },
        )


def _train_and_predict(X, y, periods: int, model: str) -> tuple[list[float], dict, str]:
    residuals = np.std(np.diff(y) / y[:-1]) * np.mean(y) if len(y) > 1 else np.mean(y) * 0.1

    if model == "xgboost":
        try:
            from xgboost import XGBRegressor

            reg = XGBRegressor(n_estimators=50, max_depth=3, learning_rate=0.1, random_state=42)
            reg.fit(X, y)
            future_X = np.arange(len(y), len(y) + periods).reshape(-1, 1)
            preds = reg.predict(future_X)
            train_pred = reg.predict(X)
            rmse = float(np.sqrt(np.mean((y - train_pred) ** 2)))
            mae = float(np.mean(np.abs(y - train_pred)))
            mape = float(np.mean(np.abs((y - train_pred) / y)) * 100)
            return list(preds), {"rmse": rmse, "mae": mae, "mape": mape, "std": residuals}, "xgboost"
        except Exception:
            pass

    if model == "lightgbm":
        try:
            import lightgbm as lgb

            reg = lgb.LGBMRegressor(n_estimators=50, max_depth=3, random_state=42, verbose=-1)
            reg.fit(X, y)
            future_X = np.arange(len(y), len(y) + periods).reshape(-1, 1)
            preds = reg.predict(future_X)
            train_pred = reg.predict(X)
            rmse = float(np.sqrt(np.mean((y - train_pred) ** 2)))
            return list(preds), {"rmse": rmse, "mae": float(np.mean(np.abs(y - train_pred))), "mape": 0, "std": residuals}, "lightgbm"
        except Exception:
            pass

    from sklearn.ensemble import GradientBoostingRegressor

    reg = GradientBoostingRegressor(n_estimators=50, max_depth=3, random_state=42)
    reg.fit(X, y)
    future_X = np.arange(len(y), len(y) + periods).reshape(-1, 1)
    preds = reg.predict(future_X)
    train_pred = reg.predict(X)
    rmse = float(np.sqrt(np.mean((y - train_pred) ** 2)))
    mae = float(np.mean(np.abs(y - train_pred)))
    mape = float(np.mean(np.abs((y - train_pred) / y)) * 100)
    return list(preds), {"rmse": rmse, "mae": mae, "mape": mape, "std": residuals}, "gradient_boosting"
