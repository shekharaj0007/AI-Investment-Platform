from fastapi import APIRouter, Query

from app.services.forecasting import ForecastingService

router = APIRouter()
_service = ForecastingService()


@router.get("/{symbol}")
async def forecast_symbol(
    symbol: str,
    metric: str = Query(default="revenue"),
    model: str = Query(default="xgboost"),
):
    return await _service.forecast(symbol, metric=metric, model=model)
