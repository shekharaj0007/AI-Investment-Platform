from fastapi import APIRouter

from app.api.v1 import (
    advisor,
    companies,
    dashboard,
    forecast,
    portfolio,
    reports,
    risk,
    sentiment,
    valuation,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(companies.router, prefix="/companies", tags=["Financial Data"])
api_router.include_router(reports.router, prefix="/reports", tags=["Annual Reports"])
api_router.include_router(companies.ratios_router, prefix="/ratios", tags=["Ratios"])
api_router.include_router(forecast.router, prefix="/forecast", tags=["Forecasting"])
api_router.include_router(risk.router, prefix="/risk", tags=["Risk"])
api_router.include_router(valuation.router, prefix="/valuation", tags=["Valuation"])
api_router.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
api_router.include_router(advisor.router, prefix="/advisor", tags=["Advisor"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
