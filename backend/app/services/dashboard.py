"""Module 12: Executive Dashboard aggregation."""

from __future__ import annotations

from app.schemas.financial import DashboardSummary, DCFInputs, PortfolioRequest
from app.services.financial_data import FinancialDataService
from app.services.forecasting import ForecastingService
from app.services.portfolio import PortfolioService
from app.services.ratios import RatioEngine
from app.services.risk import RiskService
from app.services.sentiment import SentimentService
from app.services.valuation import ValuationService


class DashboardService:
    def __init__(self) -> None:
        self._data = FinancialDataService()
        self._ratios = RatioEngine()
        self._forecast = ForecastingService()
        self._sentiment = SentimentService()
        self._risk = RiskService()
        self._valuation = ValuationService()
        self._portfolio = PortfolioService()

    async def get_summary(self, symbol: str = "AAPL") -> DashboardSummary:
        profile = await self._data.get_company_profile(symbol)
        financials = await self._data.get_financials(symbol)
        ratios = await self._ratios.compute_ratios(symbol)
        forecast = await self._forecast.forecast(symbol)
        sentiment = await self._sentiment.analyze(symbol)
        risk = await self._risk.bankruptcy_risk(symbol)
        dcf = await self._valuation.dcf(
            DCFInputs(symbol=symbol, revenue_growth=0.08, wacc=0.10, terminal_growth=0.03)
        )
        portfolio = await self._portfolio.optimize(
            PortfolioRequest(total_value=1_000_000, risk_profile="moderate")
        )

        revenue_trend = [
            {"period": s.period, "value": s.revenue or 0}
            for s in reversed(financials.income_statements[:6])
            if s.revenue
        ]
        profit_trend = [
            {"period": s.period, "value": s.net_income or 0}
            for s in reversed(financials.income_statements[:6])
            if s.net_income is not None
        ]
        cash_flow_trend = [
            {"period": s.period, "value": s.free_cash_flow or s.operating_cash_flow or 0}
            for s in reversed(financials.cash_flows[:6])
        ]

        ratio_summary = {}
        for cat in ratios.categories:
            for k, v in cat.metrics.items():
                if v is not None and k not in ("Market Cap",):
                    ratio_summary[k] = v

        recommendation = "Buy"
        if risk.ml_probability > 20 or sentiment.label == "Negative":
            recommendation = "Hold"
        if risk.ml_probability > 35:
            recommendation = "Sell"

        return DashboardSummary(
            symbol=symbol.upper(),
            company_name=profile.name,
            current_price=profile.current_price,
            market_cap=profile.market_cap,
            revenue_trend=revenue_trend,
            profit_trend=profit_trend,
            cash_flow_trend=cash_flow_trend,
            ratio_summary=ratio_summary,
            forecast_summary=forecast.forecasts,
            sentiment=sentiment,
            bankruptcy_probability=risk.ml_probability,
            fair_share_price=dcf.fair_share_price,
            portfolio_sharpe=portfolio.sharpe_ratio,
            recommendation=recommendation,
        )
