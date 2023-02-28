from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from balanced_backend.config import settings


def test_api_get_pools(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/pools")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_api_get_pools_series(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/pools/series/2/5m/1/1000")
    # This table should have no data in tests
    assert response.status_code in [204, 200]


def test_api_get_pools_dividends(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/pools/dividends")
    # This table should have no data in tests
    assert response.status_code in [204, 200]
