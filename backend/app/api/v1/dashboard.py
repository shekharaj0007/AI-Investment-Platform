from fastapi import APIRouter

from app.services.dashboard import DashboardService

router = APIRouter()
_service = DashboardService()


@router.get("/{symbol}")
async def dashboard_summary(symbol: str):
    return await _service.get_summary(symbol)
