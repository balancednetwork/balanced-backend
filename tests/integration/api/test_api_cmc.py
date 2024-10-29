import pytest
from fastapi.testclient import TestClient

from balanced_backend.config import settings


@pytest.fixture
def client(event_loop) -> TestClient:
    from balanced_backend.main_api import app
    with TestClient(app) as client:
        yield client


@pytest.mark.anyio
def test_api_get_cmc_summary(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/coin-market-cap/summary")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.anyio
def test_api_get_cmc_ticker(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/coin-market-cap/ticker")
    assert response.status_code == 200


@pytest.mark.anyio
def test_api_get_cmc_orderbook(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/coin-market-cap/orderbook/sICX_ICX")
    assert response.status_code == 200


@pytest.mark.anyio
def test_api_get_cmc_trades(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/coin-market-cap/trades/sICX_ICX")
    assert response.status_code == 200
