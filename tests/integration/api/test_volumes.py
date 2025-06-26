import pytest
from sqlalchemy.orm import Session

from balanced_backend.config import settings


@pytest.mark.anyio
async def test_api_get_volumes(client):
    """Test endpoint - must be run after one of the worker tests."""
    response = await client.get(
        f"{settings.REST_PREFIX}/contract-volumes?address=cx66d4d90f5f113eba575bf793570135f9b10cece1")
    assert response.status_code in [200, 204]
    assert len(response.json()) > 0


@pytest.mark.anyio
async def test_api_get_volumes_error(db: Session, client):
    response = await client.get(f"{settings.REST_PREFIX}/contract-volumes")
    assert response.status_code == 400
