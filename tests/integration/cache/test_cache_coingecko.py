import pytest
from balanced_backend.cache import coingecko


@pytest.mark.order(-1)
def test_update_coingecko_summary(db):
    coingecko.update_coingecko_pairs(db)


@pytest.mark.order(-1)
def test_update_coingecko_tickers(db):
    coingecko.update_coingecko_tickers(db)


@pytest.mark.order(-1)
def test_update_coingecko_order_book(db):
    coingecko.update_coingecko_orderbook(db)


@pytest.mark.order(-1)
def test_update_coingecko_historical(db):
    coingecko.update_coingecko_historical(db)
