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


@pytest.mark.anyio
@pytest.mark.parametrize("param", [
    'height=50000000',  # 50M
    'timestamp=1681839496',
])
def test_api_get_token_price(db: Session, client: TestClient, param: str):
    response = client.get(f"{settings.REST_PREFIX}/tokens/prices?symbol=sICX&{param}")
    # This table should have no data in tests
    assert response.status_code in [204, 200]


@pytest.mark.anyio
@pytest.mark.parametrize("param", [
    'height=1',
    'height=100000000000',
    'timestamp=1',
    'timestamp=100000000000',
])
def test_api_get_token_price_out_of_bounds(db: Session, client: TestClient, param: str):
    response = client.get(f"{settings.REST_PREFIX}/tokens/prices?symbol=sICX&{param}")
    # This table should have no data in tests
    assert response.status_code == 400
