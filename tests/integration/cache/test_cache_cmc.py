import pytest
from balanced_backend.cache import cmc


@pytest.mark.order(-1)
def test_update_cmc_summary(db):
    cmc.update_cmc_summary(db)


@pytest.mark.order(-1)
def test_update_cmc_tickers(db):
    cmc.update_cmc_tickers(db)


@pytest.mark.order(-1)
def test_update_cmc_order_book(db):
    cmc.update_cmc_order_book(db)


@pytest.mark.order(-1)
def test_update_cmc_trades(db):
    cmc.update_cmc_trades(db)
