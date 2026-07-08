from fastapi import APIRouter

from app.schemas.financial import AdvisorRequest, AdvisorResponse
from app.services.advisor import AdvisorService

router = APIRouter()
_service = AdvisorService()


@router.post("/ask", response_model=AdvisorResponse)
async def ask_advisor(request: AdvisorRequest) -> AdvisorResponse:
    return await _service.ask(request)
