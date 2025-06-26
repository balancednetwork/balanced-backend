import pytest

from balanced_backend.config import settings


@pytest.mark.anyio
async def test_api_get_tokens(client):
    response = await client.get(f"{settings.REST_PREFIX}/tokens")
    assert response.status_code in [200, 204]
    assert len(response.json()) > 0


@pytest.mark.anyio
async def test_api_get_token_series(client):
    response = await client.get(f"{settings.REST_PREFIX}/tokens/series/5m/1/1000?symbol=sICX")
    # This table should have no data in tests
    assert response.status_code in [204, 200]


@pytest.mark.anyio
@pytest.mark.parametrize("param", [
    'height=50000000',  # 50M
    'timestamp=1681839496',
])
async def test_api_get_token_price(client, param: str):
    response = await client.get(f"{settings.REST_PREFIX}/tokens/prices?symbol=sICX&{param}")
    # This table should have no data in tests
    assert response.status_code in [204, 200]


@pytest.mark.anyio
@pytest.mark.parametrize("param", [
    'height=1',
    'height=100000000000',
    'timestamp=1',
    'timestamp=100000000000',
])
async def test_api_get_token_price_out_of_bounds(client, param: str):
    response = await client.get(f"{settings.REST_PREFIX}/tokens/prices?symbol=sICX&{param}")
    # This table should have no data in tests
    assert response.status_code == 400
