import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_portfolio_optimize():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/portfolio/optimize",
            json={"total_value": 1_000_000, "risk_profile": "moderate", "currency": "INR"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["risk_profile"] == "moderate"
    assert len(data["allocations"]) > 0
