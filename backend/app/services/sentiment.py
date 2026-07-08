"""Module 8: News Sentiment — financial lexicon + correlation."""

from __future__ import annotations

import re

import numpy as np

from app.schemas.financial import SentimentArticle, SentimentScore
from app.services.financial_data import FinancialDataService

POSITIVE_WORDS = {
    "beat", "growth", "surge", "profit", "gain", "upgrade", "bullish", "record",
    "strong", "outperform", "raise", "expansion", "positive", "buy", "rally",
}
NEGATIVE_WORDS = {
    "miss", "loss", "decline", "fall", "cut", "downgrade", "bearish", "weak",
    "lawsuit", "investigation", "recall", "bankruptcy", "negative", "sell", "crash",
}


class SentimentService:
    def __init__(self) -> None:
        self._data = FinancialDataService()

    async def analyze(self, symbol: str) -> SentimentScore:
        news = await self._data.get_news(symbol, limit=30)
        prices = await self._data.get_stock_prices(symbol, period="3mo")

        articles: list[SentimentArticle] = []
        scores: list[float] = []

        for item in news:
            label, score = _score_text(item.title)
            articles.append(
                SentimentArticle(
                    title=item.title,
                    label=label,
                    score=round(score, 3),
                    published=item.published,
                )
            )
            scores.append(score)

        avg_score = float(np.mean(scores)) if scores else 0.0
        if avg_score > 0.15:
            overall = "Positive"
        elif avg_score < -0.15:
            overall = "Negative"
        else:
            overall = "Neutral"

        correlation = _price_correlation(scores, prices)

        timeline = []
        for i, article in enumerate(articles[:10]):
            timeline.append(
                {
                    "date": article.published or f"article_{i}",
                    "score": article.score,
                    "label": article.label,
                }
            )

        return SentimentScore(
            symbol=symbol.upper(),
            label=overall,
            score=round(avg_score, 3),
            article_count=len(articles),
            correlation_with_price=round(correlation, 3) if correlation is not None else None,
            articles=articles,
            timeline=timeline,
        )


def _score_text(text: str) -> tuple[str, float]:
    words = set(re.findall(r"[a-z]+", text.lower()))
    pos = len(words & POSITIVE_WORDS)
    neg = len(words & NEGATIVE_WORDS)
    total = pos + neg
    if total == 0:
        return "Neutral", 0.0
    score = (pos - neg) / total
    if score > 0.2:
        return "Positive", score
    if score < -0.2:
        return "Negative", score
    return "Neutral", score


def _price_correlation(sentiment_scores: list[float], prices) -> float | None:
    if len(sentiment_scores) < 3 or len(prices) < 3:
        return None
    returns = []
    for i in range(1, min(len(prices), 11)):
        if prices[i - 1].close:
            returns.append((prices[i].close - prices[i - 1].close) / prices[i - 1].close)
    n = min(len(sentiment_scores), len(returns))
    if n < 3:
        return None
    corr = float(np.corrcoef(sentiment_scores[:n], returns[:n])[0, 1])
    if corr != corr:  # NaN check
        return None
    return corr
