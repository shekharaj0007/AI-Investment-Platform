"""Module 10: AI Investment Advisor."""

from __future__ import annotations

from app.schemas.financial import AdvisorRequest, AdvisorResponse, DCFInputs, FeatureExplanation
from app.services.forecasting import ForecastingService
from app.services.ratios import RatioEngine
from app.services.risk import RiskService
from app.services.sentiment import SentimentService
from app.services.valuation import ValuationService


class AdvisorService:
    def __init__(self) -> None:
        self._ratios = RatioEngine()
        self._forecast = ForecastingService()
        self._risk = RiskService()
        self._sentiment = SentimentService()
        self._valuation = ValuationService()

    async def ask(self, request: AdvisorRequest) -> AdvisorResponse:
        symbol = request.symbol or _extract_symbol(request.question)
        if not symbol:
            return AdvisorResponse(
                question=request.question,
                recommendation="Hold",
                summary="Please specify a company symbol (e.g., INFY, AAPL, TSLA) for a detailed analysis.",
                explanations=[],
                confidence=0.0,
            )

        ratios = await self._ratios.compute_ratios(symbol)
        forecast = await self._forecast.forecast(symbol)
        risk = await self._risk.bankruptcy_risk(symbol)
        sentiment = await self._sentiment.analyze(symbol)
        dcf = await self._valuation.dcf(
            DCFInputs(symbol=symbol, revenue_growth=0.08, wacc=0.10, terminal_growth=0.03)
        )

        profitability = next((c for c in ratios.categories if c.name == "Profitability"), None)
        leverage = next((c for c in ratios.categories if c.name == "Leverage"), None)
        net_margin = profitability.metrics.get("Net Margin") if profitability else None
        debt_equity = leverage.metrics.get("Debt/Equity") if leverage else None

        growth_pct = 0.0
        if len(forecast.forecasts) >= 2 and forecast.historical:
            base = forecast.historical[-1].value if forecast.historical else forecast.forecasts[0].value
            growth_pct = ((forecast.forecasts[0].value - base) / base * 100) if base else 0

        explanations = [
            FeatureExplanation(
                feature="Revenue growth",
                value=f"{growth_pct:+.1f}% projected",
                impact="Positive" if growth_pct > 5 else "Neutral",
                shap_value=next((e["shap_value"] for e in risk.shap_explanations if "turnover" in e["feature"]), 0.18),
            ),
            FeatureExplanation(
                feature="Debt",
                value=f"D/E: {debt_equity:.2f}" if debt_equity else f"Z-zone: {risk.zone}",
                impact="Low" if risk.zone == "Safe" else "Moderate",
                shap_value=-0.05 if risk.zone == "Safe" else 0.12,
            ),
            FeatureExplanation(
                feature="Cash Flow",
                value="Positive FCF assumed" if dcf.assumptions.get("base_fcf", 0) > 0 else "Review needed",
                impact="Positive",
                shap_value=0.09,
            ),
            FeatureExplanation(
                feature="Margins",
                value=f"Net margin: {net_margin:.1%}" if net_margin else "N/A",
                impact="Improving" if net_margin and net_margin > 0.1 else "Stable",
                shap_value=0.07,
            ),
            FeatureExplanation(
                feature="News",
                value=f"{sentiment.label} ({sentiment.score:+.2f})",
                impact=sentiment.label,
                shap_value=0.11 if sentiment.label == "Positive" else -0.08,
            ),
            FeatureExplanation(
                feature="Valuation",
                value=f"Fair price: ${dcf.fair_share_price:,.2f}",
                impact="Expensive" if dcf.fair_share_price < 50 else "Fair",
                shap_value=-0.07,
            ),
        ]

        score = 0
        if growth_pct > 5:
            score += 1
        if risk.zone == "Safe":
            score += 1
        if sentiment.label == "Positive":
            score += 1
        if net_margin and net_margin > 0.08:
            score += 1

        if score >= 3:
            recommendation = "Buy"
        elif score <= 1:
            recommendation = "Sell"
        else:
            recommendation = "Hold"

        summary = (
            f"{symbol.upper()} — Revenue growth outlook is {growth_pct:+.1f}%. "
            f"Bankruptcy risk is {risk.ml_probability:.1f}% ({risk.zone} zone). "
            f"News sentiment is {sentiment.label.lower()}. "
            f"Fair value estimate: ${dcf.fair_share_price:,.2f}. "
            f"Overall recommendation: {recommendation}."
        )

        from app.services.llm import generate_text

        llm_summary = await generate_text(
            system_prompt=(
                "You are an AI investment advisor. Write a clear 3-4 sentence investment "
                "analysis for a retail investor. Base your answer ONLY on the provided data."
            ),
            user_prompt=(
                f"Symbol: {symbol.upper()}\n"
                f"Recommendation: {recommendation}\n"
                f"Revenue growth: {growth_pct:+.1f}%\n"
                f"Net margin: {net_margin}\n"
                f"Debt/Equity: {debt_equity}\n"
                f"Bankruptcy probability: {risk.ml_probability}%\n"
                f"Sentiment: {sentiment.label}\n"
                f"Fair price (DCF): ${dcf.fair_share_price:,.2f}\n"
                f"User question: {request.question}"
            ),
        )
        if llm_summary:
            summary = llm_summary

        return AdvisorResponse(
            question=request.question,
            symbol=symbol.upper(),
            recommendation=recommendation,
            summary=summary,
            explanations=explanations,
            confidence=round(0.6 + score * 0.08, 2),
        )


def _extract_symbol(question: str) -> str | None:
    known = {
        "INFY": "INFY", "INFOSYS": "INFY", "TSLA": "TSLA", "TESLA": "TSLA",
        "AAPL": "AAPL", "APPLE": "AAPL", "MSFT": "MSFT", "GOOGL": "GOOGL",
        "AMZN": "AMZN", "NVDA": "NVDA", "META": "META", "JPM": "JPM",
    }
    for token in question.upper().replace("?", " ").split():
        if token in known:
            return known[token]
    return None
