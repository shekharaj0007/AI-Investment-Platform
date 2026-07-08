"""Module 9: Portfolio Optimizer — Modern Portfolio Theory."""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

from app.schemas.financial import AssetAllocation, EfficientFrontierPoint, PortfolioRequest, PortfolioResult
from app.services.financial_data import FinancialDataService

DEFAULT_UNIVERSE = {
    "conservative": [
        ("Bonds", "BND", 0.06, 0.05),
        ("ETFs", "SPY", 0.10, 0.15),
        ("Gold", "GLD", 0.08, 0.12),
        ("Stocks", "JNJ", 0.07, 0.14),
    ],
    "moderate": [
        ("Stocks", "INFY", 0.14, 0.22),
        ("Stocks", "AAPL", 0.12, 0.25),
        ("ETFs", "SPY", 0.10, 0.15),
        ("Bonds", "BND", 0.06, 0.05),
        ("Gold", "GLD", 0.08, 0.12),
    ],
    "aggressive": [
        ("Stocks", "TSLA", 0.20, 0.45),
        ("Stocks", "NVDA", 0.25, 0.40),
        ("Stocks", "AMZN", 0.15, 0.30),
        ("ETFs", "QQQ", 0.12, 0.22),
        ("Gold", "GLD", 0.08, 0.12),
    ],
}


class PortfolioService:
    def __init__(self) -> None:
        self._data = FinancialDataService()

    async def optimize(self, request: PortfolioRequest) -> PortfolioResult:
        profile = request.risk_profile.lower()
        universe = DEFAULT_UNIVERSE.get(profile, DEFAULT_UNIVERSE["moderate"])

        if request.symbols:
            universe = await self._build_from_symbols(request.symbols)

        n = len(universe)
        expected_returns = np.array([u[2] for u in universe])
        volatilities = np.array([u[3] for u in universe])
        corr = np.full((n, n), 0.3)
        np.fill_diagonal(corr, 1.0)
        cov = np.outer(volatilities, volatilities) * corr

        target_vol = {"conservative": 0.08, "moderate": 0.14, "aggressive": 0.22}[profile]

        def neg_sharpe(w):
            ret = w @ expected_returns
            vol = np.sqrt(w @ cov @ w)
            return -(ret - 0.04) / max(vol, 0.001)

        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
        bounds = [(0.05, 0.6) for _ in range(n)]
        x0 = np.ones(n) / n
        result = minimize(neg_sharpe, x0, method="SLSQP", bounds=bounds, constraints=constraints)
        weights = result.x if result.success else x0

        port_return = float(weights @ expected_returns)
        port_vol = float(np.sqrt(weights @ cov @ weights))
        sharpe = (port_return - 0.04) / max(port_vol, 0.001)

        allocations = [
            AssetAllocation(
                asset_class=asset_class,
                symbol=symbol,
                weight=round(float(w), 4),
                amount=round(request.total_value * float(w), 2),
                expected_return=round(ret, 4),
            )
            for (asset_class, symbol, ret, _), w in zip(universe, weights, strict=False)
            if w > 0.01
        ]

        frontier = self._efficient_frontier(expected_returns, cov)

        return PortfolioResult(
            total_value=request.total_value,
            risk_profile=profile,
            expected_return=round(port_return, 4),
            volatility=round(port_vol, 4),
            sharpe_ratio=round(sharpe, 2),
            allocations=allocations,
            efficient_frontier=frontier,
        )

    async def _build_from_symbols(self, symbols: list[str]) -> list[tuple]:
        universe = []
        for sym in symbols[:6]:
            try:
                prices = await self._data.get_stock_prices(sym, period="1y")
                if len(prices) < 10:
                    continue
                closes = [p.close for p in prices]
                returns = [(closes[i] - closes[i - 1]) / closes[i - 1] for i in range(1, len(closes))]
                ret = float(np.mean(returns)) * 252
                vol = float(np.std(returns)) * np.sqrt(252)
                profile = await self._data.get_company_profile(sym)
                universe.append(("Stocks", sym, max(ret, 0.05), max(vol, 0.1)))
            except Exception:
                continue
        return universe or DEFAULT_UNIVERSE["moderate"]

    def _efficient_frontier(self, expected_returns, cov, points: int = 5) -> list[EfficientFrontierPoint]:
        frontier = []
        n = len(expected_returns)
        for target in np.linspace(expected_returns.min(), expected_returns.max(), points):
            constraints = [
                {"type": "eq", "fun": lambda w: np.sum(w) - 1},
                {"type": "eq", "fun": lambda w, t=target: w @ expected_returns - t},
            ]
            bounds = [(0, 1) for _ in range(n)]
            x0 = np.ones(n) / n

            def portfolio_vol(w):
                return np.sqrt(w @ cov @ w)

            res = minimize(portfolio_vol, x0, method="SLSQP", bounds=bounds, constraints=constraints)
            if res.success:
                vol = float(res.fun)
                ret = float(res.x @ expected_returns)
                sharpe = (ret - 0.04) / max(vol, 0.001)
                frontier.append(
                    EfficientFrontierPoint(
                        volatility=round(vol, 4),
                        expected_return=round(ret, 4),
                        sharpe_ratio=round(sharpe, 2),
                    )
                )
        return frontier
