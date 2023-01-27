from balanced_backend.utils.band import (
    get_band_icx_price,
)


def test_get_band_icx_price():
    price = get_band_icx_price()
    assert isinstance(price, float)

    price = get_band_icx_price(height=61051149)
    assert price == 0.2146
