from fastapi import APIRouter

from app.schemas.financial import PortfolioRequest, PortfolioResult
from app.services.portfolio import PortfolioService

router = APIRouter()
_service = PortfolioService()


@router.post("/optimize", response_model=PortfolioResult)
async def optimize_portfolio(request: PortfolioRequest) -> PortfolioResult:
    return await _service.optimize(request)
