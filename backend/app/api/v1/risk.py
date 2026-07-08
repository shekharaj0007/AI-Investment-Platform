from fastapi import APIRouter

from app.services.risk import RiskService

router = APIRouter()
_service = RiskService()


@router.get("/bankruptcy/{symbol}")
async def bankruptcy_risk(symbol: str):
    return await _service.bankruptcy_risk(symbol)


@router.get("/credit/{symbol}")
async def credit_risk(symbol: str):
    return await _service.credit_risk(symbol)
