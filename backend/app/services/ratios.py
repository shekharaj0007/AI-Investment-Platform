"""Module 3: Financial Ratio Engine."""

from __future__ import annotations

from datetime import date

from app.schemas.financial import RatioAnalysis, RatioCategory, RatioHistoryPoint
from app.services.financial_data import FinancialDataService


class RatioEngine:
    def __init__(self) -> None:
        self._data = FinancialDataService()

    async def compute_ratios(self, symbol: str) -> RatioAnalysis:
        financials = await self._data.get_financials(symbol)
        profile = await self._data.get_company_profile(symbol)

        income_list = financials.income_statements
        balance_list = financials.balance_sheets
        income = income_list[0] if income_list else None
        balance = balance_list[0] if balance_list else None

        revenue = income.revenue if income else None
        net_income = income.net_income if income else None
        gross_profit = income.gross_profit if income else None
        ebit = income.ebit if income else None
        total_assets = balance.total_assets if balance else None
        total_equity = balance.total_equity if balance else None
        total_debt = balance.total_debt if balance else None
        current_assets = balance.current_assets if balance else None
        current_liabilities = balance.current_liabilities if balance else None
        inventory = balance.inventory if balance else None

        capital_employed = None
        if total_equity is not None or total_debt is not None:
            capital_employed = (total_equity or 0) + (total_debt or 0) or None

        interest_expense = None
        if ebit and net_income:
            interest_expense = max(ebit - net_income, 1)

        categories = [
            RatioCategory(
                name="Profitability",
                metrics={
                    "ROE": _ratio(net_income, total_equity),
                    "ROA": _ratio(net_income, total_assets),
                    "ROCE": _ratio(ebit or net_income, capital_employed),
                    "Gross Margin": _ratio(gross_profit, revenue),
                    "Net Margin": _ratio(net_income, revenue),
                    "EBIT Margin": _ratio(ebit, revenue),
                },
            ),
            RatioCategory(
                name="Liquidity",
                metrics={
                    "Current Ratio": _ratio(current_assets, current_liabilities),
                    "Quick Ratio": _ratio(
                        (current_assets or 0) - (inventory or 0) if current_assets else None,
                        current_liabilities,
                    ),
                },
            ),
            RatioCategory(
                name="Leverage",
                metrics={
                    "Debt/Equity": _ratio(total_debt, total_equity),
                    "Debt/Assets": _ratio(total_debt, total_assets),
                    "Interest Coverage": _ratio(ebit, interest_expense),
                },
            ),
            RatioCategory(
                name="Efficiency",
                metrics={
                    "Asset Turnover": _ratio(revenue, total_assets),
                    "Inventory Turnover": _ratio(revenue, inventory),
                    "Equity Multiplier": _ratio(total_assets, total_equity),
                },
            ),
            RatioCategory(
                name="Valuation",
                metrics={
                    "P/E": profile.pe_ratio,
                    "P/B": profile.pb_ratio,
                    "Market Cap": profile.market_cap,
                    "EV/EBITDA": _ratio(profile.market_cap, ebit),
                },
            ),
        ]

        history = []
        for i in range(min(len(income_list), len(balance_list), 4)):
            inc = income_list[i]
            bal = balance_list[i]
            history.append(
                RatioHistoryPoint(
                    period=inc.period,
                    metrics={
                        "Net Margin": _ratio(inc.net_income, inc.revenue),
                        "ROE": _ratio(inc.net_income, bal.total_equity),
                        "Current Ratio": _ratio(bal.current_assets, bal.current_liabilities),
                        "Debt/Equity": _ratio(bal.total_debt, bal.total_equity),
                    },
                )
            )

        return RatioAnalysis(
            symbol=symbol.upper(),
            as_of=date.today().isoformat(),
            categories=categories,
            history=history,
        )


def _ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return round(numerator / denominator, 4)
