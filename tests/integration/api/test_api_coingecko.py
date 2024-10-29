import pytest
from fastapi.testclient import TestClient

from balanced_backend.config import settings

@pytest.fixture
def client(event_loop) -> TestClient:
    from balanced_backend.main_api import app
    with TestClient(app) as client:
        yield client


@pytest.mark.anyio
def test_api_get_coingecko_summary(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/coingecko/pairs")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.anyio
def test_api_get_coingecko_ticker(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/coingecko/tickers")
    assert response.status_code == 200


@pytest.mark.anyio
def test_api_get_coingecko_orderbook(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/coingecko/orderbook")
    assert response.status_code == 200


@pytest.mark.anyio
def test_api_get_coingecko_orderbook_ticker(client: TestClient):
    response = client.get(
        f"{settings.REST_PREFIX}/coingecko/orderbook?ticker_id=sICX_bnUSD"
    )
    assert response.status_code == 200


@pytest.mark.anyio
def test_api_get_coingecko_trades(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/coingecko/historical_trades")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.anyio
def test_api_get_coingecko_trades_ticker(client: TestClient):
    response = client.get(
        f"{settings.REST_PREFIX}/coingecko/historical_trades?ticker_id=sICX_bnUSD"
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.anyio
def test_api_get_coingecko_trades_type(client: TestClient):
    response = client.get(
        f"{settings.REST_PREFIX}/coingecko/historical_trades?type=buy"
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.anyio
def test_api_get_coingecko_trades_type_ticker(client: TestClient):
    response = client.get(
        f"{settings.REST_PREFIX}/coingecko/historical_trades?type=buy&ticker_id=sICX_bnUSD"
    )
    assert response.status_code == 200
    # TODO: Needs hydrated db to not be flakey
    # assert len(response.json()) > 0


@pytest.mark.anyio
def test_api_get_coingecko_trades_bad_type(client: TestClient):
    response = client.get(
        f"{settings.REST_PREFIX}/coingecko/historical_trades?type=wtf"
    )
    assert response.status_code == 422


@pytest.mark.anyio
def test_api_get_coingecko_trades_bad_ticker_id(client: TestClient):
    response = client.get(
        f"{settings.REST_PREFIX}/coingecko/historical_trades?ticker_id=wtf"
    )
    assert response.status_code == 422
