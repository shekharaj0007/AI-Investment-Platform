"""Demo financial data when live Yahoo Finance is unavailable."""

from __future__ import annotations

DEMO_PROFILES = {
    "AAPL": {
        "name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "market_cap": 3_400_000_000_000,
        "current_price": 227.5,
        "pe_ratio": 34.2,
        "pb_ratio": 52.1,
        "currency": "USD",
    },
    "TSLA": {
        "name": "Tesla, Inc.",
        "sector": "Consumer Cyclical",
        "industry": "Auto Manufacturers",
        "market_cap": 800_000_000_000,
        "current_price": 248.0,
        "pe_ratio": 62.5,
        "pb_ratio": 12.3,
        "currency": "USD",
    },
    "INFY": {
        "name": "Infosys Limited",
        "sector": "Technology",
        "industry": "Information Technology Services",
        "market_cap": 85_000_000_000,
        "current_price": 20.5,
        "pe_ratio": 25.8,
        "pb_ratio": 8.2,
        "currency": "USD",
    },
    "MSFT": {
        "name": "Microsoft Corporation",
        "sector": "Technology",
        "industry": "Software",
        "market_cap": 3_100_000_000_000,
        "current_price": 415.0,
        "pe_ratio": 36.0,
        "pb_ratio": 12.0,
        "currency": "USD",
    },
}

DEMO_INCOME = {
    "AAPL": [
        {"period": "2024-09-30", "revenue": 391_035_000_000, "gross_profit": 180_683_000_000, "net_income": 93_736_000_000, "ebit": 123_216_000_000, "eps": 6.11},
        {"period": "2023-09-30", "revenue": 383_285_000_000, "gross_profit": 169_148_000_000, "net_income": 96_995_000_000, "ebit": 114_301_000_000, "eps": 6.16},
        {"period": "2022-09-30", "revenue": 394_328_000_000, "gross_profit": 170_782_000_000, "net_income": 99_803_000_000, "ebit": 119_437_000_000, "eps": 6.15},
        {"period": "2021-09-30", "revenue": 365_817_000_000, "gross_profit": 152_836_000_000, "net_income": 94_680_000_000, "ebit": 108_949_000_000, "eps": 5.67},
    ],
    "TSLA": [
        {"period": "2024-12-31", "revenue": 97_690_000_000, "gross_profit": 17_660_000_000, "net_income": 7_130_000_000, "ebit": 7_760_000_000, "eps": 2.04},
        {"period": "2023-12-31", "revenue": 96_773_000_000, "gross_profit": 17_660_000_000, "net_income": 14_999_000_000, "ebit": 8_891_000_000, "eps": 4.31},
    ],
    "INFY": [
        {"period": "2024-03-31", "revenue": 18_562_000_000, "gross_profit": 6_200_000_000, "net_income": 2_941_000_000, "ebit": 3_400_000_000, "eps": 0.71},
        {"period": "2023-03-31", "revenue": 17_314_000_000, "gross_profit": 5_800_000_000, "net_income": 2_659_000_000, "ebit": 3_100_000_000, "eps": 0.64},
    ],
}

DEMO_BALANCE = {
    "AAPL": [
        {"period": "2024-09-30", "total_assets": 364_980_000_000, "total_debt": 106_629_000_000, "total_equity": 56_950_000_000, "current_assets": 152_987_000_000, "current_liabilities": 176_392_000_000, "inventory": 7_286_000_000},
        {"period": "2023-09-30", "total_assets": 352_583_000_000, "total_debt": 111_088_000_000, "total_equity": 62_146_000_000, "current_assets": 143_566_000_000, "current_liabilities": 145_308_000_000, "inventory": 6_331_000_000},
    ],
    "TSLA": [
        {"period": "2024-12-31", "total_assets": 122_070_000_000, "total_debt": 9_570_000_000, "total_equity": 73_210_000_000, "current_assets": 58_360_000_000, "current_liabilities": 31_590_000_000, "inventory": 12_020_000_000},
    ],
    "INFY": [
        {"period": "2024-03-31", "total_assets": 14_780_000_000, "total_debt": 890_000_000, "total_equity": 10_120_000_000, "current_assets": 8_450_000_000, "current_liabilities": 3_210_000_000, "inventory": 0},
    ],
}

DEMO_CASHFLOW = {
    "AAPL": [
        {"period": "2024-09-30", "operating_cash_flow": 118_254_000_000, "free_cash_flow": 108_807_000_000},
        {"period": "2023-09-30", "operating_cash_flow": 110_543_000_000, "free_cash_flow": 99_584_000_000},
    ],
    "TSLA": [
        {"period": "2024-12-31", "operating_cash_flow": 14_720_000_000, "free_cash_flow": 3_580_000_000},
    ],
    "INFY": [
        {"period": "2024-03-31", "operating_cash_flow": 3_200_000_000, "free_cash_flow": 2_900_000_000},
    ],
}

DEMO_NEWS = {
    "AAPL": [
        {"title": "Apple beats earnings expectations with strong iPhone sales", "publisher": "Reuters", "published": "2025-01-30"},
        {"title": "Apple services revenue hits record high", "publisher": "Bloomberg", "published": "2025-01-28"},
        {"title": "Analysts upgrade Apple on AI integration outlook", "publisher": "CNBC", "published": "2025-01-25"},
        {"title": "Apple margin expansion continues in Q1", "publisher": "WSJ", "published": "2025-01-20"},
    ],
    "TSLA": [
        {"title": "Tesla delivery numbers beat street estimates", "publisher": "Reuters", "published": "2025-01-29"},
        {"title": "Tesla faces margin pressure from price cuts", "publisher": "Bloomberg", "published": "2025-01-22"},
    ],
    "INFY": [
        {"title": "Infosys reports steady revenue growth in Q3", "publisher": "Economic Times", "published": "2025-01-15"},
        {"title": "Infosys wins large deal from global bank", "publisher": "Reuters", "published": "2025-01-10"},
    ],
}

DEFAULT_SYMBOL = "AAPL"


def get_demo_profile(symbol: str) -> dict:
    sym = symbol.upper()
    base = DEMO_PROFILES.get(sym, DEMO_PROFILES[DEFAULT_SYMBOL]).copy()
    base["symbol"] = sym
    if sym not in DEMO_PROFILES:
        base["name"] = f"{sym} Corporation"
    return base


def get_demo_income(symbol: str) -> list[dict]:
    return DEMO_INCOME.get(symbol.upper(), DEMO_INCOME[DEFAULT_SYMBOL])


def get_demo_balance(symbol: str) -> list[dict]:
    return DEMO_BALANCE.get(symbol.upper(), DEMO_BALANCE[DEFAULT_SYMBOL])


def get_demo_cashflow(symbol: str) -> list[dict]:
    return DEMO_CASHFLOW.get(symbol.upper(), DEMO_CASHFLOW[DEFAULT_SYMBOL])


def get_demo_news(symbol: str) -> list[dict]:
    return DEMO_NEWS.get(symbol.upper(), DEMO_NEWS[DEFAULT_SYMBOL])


def get_demo_prices(symbol: str) -> list[dict]:
    import random

    random.seed(hash(symbol) % 10000)
    price = DEMO_PROFILES.get(symbol.upper(), DEMO_PROFILES[DEFAULT_SYMBOL])["current_price"]
    points = []
    for i in range(252):
        price *= 1 + random.uniform(-0.02, 0.025)
        points.append({"date": f"2024-{min(i//21+1,12):02d}-{(i%28)+1:02d}", "close": round(price, 2), "volume": random.randint(1_000_000, 50_000_000)})
    return points[-60:]
