import pytest
from balanced_backend.config import settings


@pytest.mark.anyio
async def test_api_get_loans_chart(client):
    """Test endpoint - must be run after one of the worker tests."""
    response = await client.get(
        f"{settings.REST_PREFIX}/contract-methods?address=cx66d4d90f5f113eba575bf793570135f9b10cece1")
    assert response.status_code in [200, 204]
    assert len(response.json()) > 0


@pytest.mark.anyio
async def test_api_get_loans_chart_error(client):
    response = await client.get(f"{settings.REST_PREFIX}/contract-methods")
    assert response.status_code == 400
