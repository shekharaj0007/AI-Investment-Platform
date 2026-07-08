"""Module 1: Financial Data Collection with live Yahoo Finance + demo fallback."""

from __future__ import annotations

import os

from app.core.cache import cache_get, cache_set
from app.data import demo_data
from app.schemas.financial import (
    CompanyDataBundle,
    CompanyFinancials,
    CompanyProfile,
    FinancialStatement,
    NewsItem,
    StockPricePoint,
)


USE_LIVE_DATA = os.getenv("USE_LIVE_DATA", "false").lower() == "true"


class FinancialDataService:
    async def get_company_profile(self, symbol: str) -> CompanyProfile:
        cache_key = f"profile:{symbol.upper()}"
        cached = await cache_get(cache_key)
        if cached:
            return CompanyProfile(**cached)

        profile = await self._fetch_profile(symbol)
        await cache_set(cache_key, profile.model_dump(), ttl=1800)
        return profile

    async def get_financials(self, symbol: str) -> CompanyFinancials:
        cache_key = f"financials:{symbol.upper()}"
        cached = await cache_get(cache_key)
        if cached:
            return CompanyFinancials(**cached)

        financials = await self._fetch_financials(symbol)
        await cache_set(cache_key, financials.model_dump(), ttl=3600)
        return financials

    async def get_stock_prices(self, symbol: str, period: str = "1y") -> list[StockPricePoint]:
        cache_key = f"prices:{symbol.upper()}:{period}"
        cached = await cache_get(cache_key)
        if cached:
            return [StockPricePoint(**p) for p in cached]

        points = await self._fetch_prices(symbol, period)
        await cache_set(cache_key, [p.model_dump() for p in points], ttl=900)
        return points

    async def get_news(self, symbol: str, limit: int = 20) -> list[NewsItem]:
        cache_key = f"news:{symbol.upper()}"
        cached = await cache_get(cache_key)
        if cached:
            return [NewsItem(**n) for n in cached[:limit]]

        items = await self._fetch_news(symbol, limit)
        await cache_set(cache_key, [n.model_dump() for n in items], ttl=600)
        return items

    async def get_full_bundle(self, symbol: str) -> CompanyDataBundle:
        profile = await self.get_company_profile(symbol)
        financials = await self.get_financials(symbol)
        prices = await self.get_stock_prices(symbol)
        news = await self.get_news(symbol)
        return CompanyDataBundle(profile=profile, financials=financials, stock_prices=prices, news=news)

    async def _fetch_profile(self, symbol: str) -> CompanyProfile:
        if USE_LIVE_DATA:
            try:
                import yfinance as yf

                info = yf.Ticker(symbol).info or {}
                if info.get("regularMarketPrice") or info.get("marketCap"):
                    return CompanyProfile(
                        symbol=symbol.upper(),
                        name=info.get("longName") or info.get("shortName") or symbol,
                        sector=info.get("sector"),
                        industry=info.get("industry"),
                        market_cap=info.get("marketCap"),
                        currency=info.get("currency", "USD"),
                        current_price=info.get("currentPrice") or info.get("regularMarketPrice"),
                        pe_ratio=info.get("trailingPE"),
                        pb_ratio=info.get("priceToBook"),
                        dividend_yield=info.get("dividendYield"),
                        fifty_two_week_high=info.get("fiftyTwoWeekHigh"),
                        fifty_two_week_low=info.get("fiftyTwoWeekLow"),
                    )
            except Exception:
                pass
        d = demo_data.get_demo_profile(symbol)
        return CompanyProfile(**d)

    async def _fetch_financials(self, symbol: str) -> CompanyFinancials:
        if USE_LIVE_DATA:
            try:
                import yfinance as yf

                ticker = yf.Ticker(symbol)
                income = _parse_income(ticker.financials)
                balance = _parse_balance(ticker.balance_sheet)
                cashflow = _parse_cashflow(ticker.cashflow)
                if income or balance:
                    return CompanyFinancials(
                        symbol=symbol.upper(),
                        income_statements=income,
                        balance_sheets=balance,
                        cash_flows=cashflow,
                    )
            except Exception:
                pass
        return CompanyFinancials(
            symbol=symbol.upper(),
            income_statements=[FinancialStatement(**s) for s in demo_data.get_demo_income(symbol)],
            balance_sheets=[FinancialStatement(**s) for s in demo_data.get_demo_balance(symbol)],
            cash_flows=[FinancialStatement(**s) for s in demo_data.get_demo_cashflow(symbol)],
        )

    async def _fetch_prices(self, symbol: str, period: str) -> list[StockPricePoint]:
        if USE_LIVE_DATA:
            try:
                import yfinance as yf

                hist = yf.Ticker(symbol).history(period=period)
                if not hist.empty:
                    points = []
                    for idx, row in hist.iterrows():
                        points.append(
                            StockPricePoint(
                                date=idx.strftime("%Y-%m-%d"),
                                open=_f(row.get("Open")),
                                high=_f(row.get("High")),
                                low=_f(row.get("Low")),
                                close=_f(row.get("Close")) or 0.0,
                                volume=_f(row.get("Volume")),
                            )
                        )
                    return points
            except Exception:
                pass
        return [StockPricePoint(**p) for p in demo_data.get_demo_prices(symbol)]

    async def _fetch_news(self, symbol: str, limit: int) -> list[NewsItem]:
        if USE_LIVE_DATA:
            try:
                import yfinance as yf

                raw = yf.Ticker(symbol).news or []
                if raw:
                    items = []
                    for article in raw[:limit]:
                        content = article.get("content", article)
                        items.append(
                            NewsItem(
                                title=content.get("title", article.get("title", "")),
                                publisher=(content.get("provider") or {}).get("displayName"),
                                link=content.get("canonicalUrl") or content.get("clickThroughUrl"),
                                published=str(content.get("pubDate") or ""),
                            )
                        )
                    return items
            except Exception:
                pass
        return [NewsItem(**n) for n in demo_data.get_demo_news(symbol)[:limit]]


def _parse_income(frame) -> list[FinancialStatement]:
    if frame is None or frame.empty:
        return []
    statements = []
    for col in frame.columns:
        period = col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col)
        row = frame[col]
        statements.append(
            FinancialStatement(
                period=period,
                revenue=_safe(row, "Total Revenue"),
                gross_profit=_safe(row, "Gross Profit"),
                net_income=_safe(row, "Net Income"),
                ebit=_safe(row, "EBIT") or _safe(row, "Operating Income"),
                eps=_safe(row, "Basic EPS"),
            )
        )
    return statements


def _parse_balance(frame) -> list[FinancialStatement]:
    if frame is None or frame.empty:
        return []
    statements = []
    for col in frame.columns:
        period = col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col)
        row = frame[col]
        statements.append(
            FinancialStatement(
                period=period,
                total_assets=_safe(row, "Total Assets"),
                total_debt=_safe(row, "Total Debt"),
                total_equity=_safe(row, "Stockholders Equity"),
                current_assets=_safe(row, "Current Assets"),
                current_liabilities=_safe(row, "Current Liabilities"),
                inventory=_safe(row, "Inventory"),
            )
        )
    return statements


def _parse_cashflow(frame) -> list[FinancialStatement]:
    if frame is None or frame.empty:
        return []
    statements = []
    for col in frame.columns:
        period = col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col)
        row = frame[col]
        statements.append(
            FinancialStatement(
                period=period,
                operating_cash_flow=_safe(row, "Operating Cash Flow"),
                free_cash_flow=_safe(row, "Free Cash Flow"),
            )
        )
    return statements


def _safe(row, key: str) -> float | None:
    try:
        val = row.get(key)
        if val is None or str(val) == "nan":
            return None
        return float(val)
    except (TypeError, ValueError, KeyError):
        return None


def _f(val) -> float | None:
    if val is None or str(val) == "nan":
        return None
    return float(val)
