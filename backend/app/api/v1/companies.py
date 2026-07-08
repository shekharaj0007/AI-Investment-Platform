from fastapi import APIRouter, Query

from app.schemas.financial import CompanyDataBundle, CompanyFinancials, CompanyProfile, NewsItem, StockPricePoint
from app.services.financial_data import FinancialDataService

router = APIRouter()
ratios_router = APIRouter()

_data = FinancialDataService()


@router.get("/{symbol}", response_model=CompanyProfile)
async def get_company(symbol: str) -> CompanyProfile:
    return await _data.get_company_profile(symbol)


@router.get("/{symbol}/financials", response_model=CompanyFinancials)
async def get_financials(symbol: str) -> CompanyFinancials:
    return await _data.get_financials(symbol)


@router.get("/{symbol}/prices", response_model=list[StockPricePoint])
async def get_prices(symbol: str, period: str = Query(default="1y")) -> list[StockPricePoint]:
    return await _data.get_stock_prices(symbol, period=period)


@router.get("/{symbol}/news", response_model=list[NewsItem])
async def get_news(symbol: str, limit: int = Query(default=20, le=50)) -> list[NewsItem]:
    return await _data.get_news(symbol, limit=limit)


@router.get("/{symbol}/bundle", response_model=CompanyDataBundle)
async def get_bundle(symbol: str) -> CompanyDataBundle:
    return await _data.get_full_bundle(symbol)


@ratios_router.get("/{symbol}")
async def get_ratios(symbol: str):
    from app.services.ratios import RatioEngine

    return await RatioEngine().compute_ratios(symbol)
