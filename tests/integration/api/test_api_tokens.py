import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from balanced_backend.config import settings


@pytest.mark.anyio
def test_api_get_tokens(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/tokens")
    assert response.status_code in [200, 204]
    assert len(response.json()) > 0


@pytest.mark.anyio
def test_api_get_token_series(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/tokens/series/5m/1/1000?symbol=sICX")
    # This table should have no data in tests
    assert response.status_code in [204, 200]
