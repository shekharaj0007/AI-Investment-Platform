"""Modules 5 & 6: Bankruptcy and Credit Risk with ML + SHAP."""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from app.ml.explainability import compute_shap_explanations
from app.schemas.financial import BankruptcyRisk, CreditRisk
from app.services.financial_data import FinancialDataService

# Synthetic training data based on Altman Z-score zones
_TRAINING_X = np.array(
    [
        [2.5, 0.15, 0.12, 1.8, 1.2],
        [2.0, 0.10, 0.08, 1.4, 1.0],
        [1.5, 0.05, 0.04, 1.0, 0.8],
        [1.0, -0.02, 0.02, 0.7, 0.5],
        [0.5, -0.10, -0.05, 0.4, 0.3],
        [3.0, 0.20, 0.15, 2.0, 1.5],
        [0.2, -0.15, -0.10, 0.2, 0.2],
    ]
)
_TRAINING_Y = np.array([0, 0, 0, 1, 1, 0, 1])
_FEATURE_NAMES = [
    "working_capital_ratio",
    "retained_earnings_ratio",
    "ebit_ratio",
    "market_value_leverage",
    "asset_turnover",
]
_RISK_MODEL = RandomForestClassifier(n_estimators=50, random_state=42)
_RISK_MODEL.fit(_TRAINING_X, _TRAINING_Y)


class RiskService:
    def __init__(self) -> None:
        self._data = FinancialDataService()

    async def bankruptcy_risk(self, symbol: str) -> BankruptcyRisk:
        features = await self._extract_features(symbol)
        z = self._altman_z(features)
        zone = "Safe" if z > 2.99 else "Grey" if z > 1.81 else "Distress"

        X = np.array([[features[name] for name in _FEATURE_NAMES]])
        prob = float(_RISK_MODEL.predict_proba(X)[0][1]) * 100
        shap_exp = compute_shap_explanations(_RISK_MODEL, X, _FEATURE_NAMES)

        public_factors = {k: round(v, 4) for k, v in features.items() if not k.startswith("_")}

        return BankruptcyRisk(
            symbol=symbol.upper(),
            altman_z_score=round(z, 3),
            zone=zone,
            ml_probability=round(prob, 2),
            model="altman_z + random_forest",
            factors=public_factors,
            shap_explanations=shap_exp,
        )

    async def credit_risk(self, symbol: str) -> CreditRisk:
        bankruptcy = await self.bankruptcy_risk(symbol)
        prob = bankruptcy.ml_probability / 100

        if prob < 0.03:
            rating = "AAA"
        elif prob < 0.07:
            rating = "AA"
        elif prob < 0.12:
            rating = "A"
        elif prob < 0.20:
            rating = "BBB"
        else:
            rating = "BB"

        return CreditRisk(
            symbol=symbol.upper(),
            predicted_rating=rating,
            default_probability=bankruptcy.ml_probability,
            confidence=round(0.95 - prob * 0.5, 2),
            feature_contributions=bankruptcy.factors,
            shap_explanations=bankruptcy.shap_explanations,
        )

    async def _extract_features(self, symbol: str) -> dict[str, float]:
        financials = await self._data.get_financials(symbol)
        profile = await self._data.get_company_profile(symbol)
        income = financials.income_statements[0] if financials.income_statements else None
        balance = financials.balance_sheets[0] if financials.balance_sheets else None

        total_assets = balance.total_assets or 1.0
        total_liabilities = balance.total_debt or 1.0
        working_capital = (balance.current_assets or 0) - (balance.current_liabilities or 0)
        retained_earnings = balance.total_equity or 0
        ebit = (income.ebit or income.net_income or 0) if income else 0
        revenue = (income.revenue or 1.0) if income else 1.0
        market_cap = profile.market_cap or total_assets

        return {
            "working_capital_ratio": working_capital / total_assets,
            "retained_earnings_ratio": retained_earnings / total_assets,
            "ebit_ratio": ebit / total_assets,
            "market_value_leverage": total_assets / max(total_liabilities, 1),
            "asset_turnover": revenue / total_assets,
            "_market_cap": market_cap,
        }

    def _altman_z(self, features: dict[str, float]) -> float:
        return (
            1.2 * features["working_capital_ratio"]
            + 1.4 * features["retained_earnings_ratio"]
            + 3.3 * features["ebit_ratio"]
            + 0.6 * features["market_value_leverage"]
            + 1.0 * features["asset_turnover"]
        )
