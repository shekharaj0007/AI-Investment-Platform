from fastapi import APIRouter

from app.schemas.financial import DCFInputs, DCFResult
from app.services.valuation import ValuationService

router = APIRouter()
_service = ValuationService()


@router.post("/dcf", response_model=DCFResult)
async def run_dcf(inputs: DCFInputs) -> DCFResult:
    return await _service.dcf(inputs)


@router.get("/comps/{symbol}")
async def get_comparables(symbol: str):
    result = await _service.dcf(
        DCFInputs(symbol=symbol, revenue_growth=0.08, wacc=0.10, terminal_growth=0.03)
    )
    return {"symbol": symbol, "comparables": result.comparables, "fair_share_price": result.fair_share_price}
