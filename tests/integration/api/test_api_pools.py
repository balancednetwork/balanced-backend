import pytest

from balanced_backend.config import settings


@pytest.mark.anyio
async def test_api_get_pools(client):
    response = await client.get(f"{settings.REST_PREFIX}/pools")
    assert response.status_code in [200, 204]
    assert len(response.json()) > 0


@pytest.mark.anyio
async def test_api_get_pools_series(client):
    response = await client.get(f"{settings.REST_PREFIX}/pools/series/2/5m/1/1000")
    # This table should have no data in tests
    assert response.status_code in [204, 200]


@pytest.mark.anyio
async def test_api_get_pools_dividends(client):
    response = await client.get(f"{settings.REST_PREFIX}/pools/dividends")
    # This table should have no data in tests
    assert response.status_code in [204, 200]


@pytest.mark.parametrize(
    "token_a,token_b,interval,start,end",
    [
        (
            "cx88fd7df7ddff82f7cc735c871dc519838cb235bb",
            "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619",
            "1h",
            "1716785596",  # 12h
            "1716828796",
        ),
    ],
)
@pytest.mark.anyio
async def test_api_get_pools_dividends(client, token_a, token_b, interval, start, end):
    response = await client.get(
        f"{settings.REST_PREFIX}/pools/series/implied/{token_a}/{token_b}/{interval}/{start}/{end}"
    )
    # This table should have no data in tests
    assert response.status_code in [204, 200]
