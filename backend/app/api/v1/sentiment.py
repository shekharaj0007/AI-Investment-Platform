from fastapi import APIRouter

from app.services.sentiment import SentimentService

router = APIRouter()
_service = SentimentService()


@router.get("/{symbol}")
async def sentiment_analysis(symbol: str):
    return await _service.analyze(symbol)
