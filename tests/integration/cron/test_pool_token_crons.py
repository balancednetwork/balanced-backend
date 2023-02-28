from sqlmodel import select

from balanced_backend.tables.pools import Pool
from balanced_backend.tables.tokens import Token
from balanced_backend.cron.pool_lists import run_pool_list
from balanced_backend.cron.token_lists import run_token_list
from balanced_backend.cron.pool_prices import run_pool_prices
from balanced_backend.cron.token_price import run_token_pool_prices
#
#   NOTE: Tests must be run in order - cron scheduler forces this
#

def test_run_token_list(db):
    with db as session:
        run_token_list(session=db)
        result = session.execute(select(Token))
        tokens = result.scalars().all()

    assert len(tokens) > 30


def test_run_pool_list(db):
    with db as session:
        run_pool_list(session=db)
        result = session.execute(select(Pool))
        pools = result.scalars().all()

    assert len(pools) > 30


def test_run_pool_prices(db):
    with db as session:
        run_pool_prices(session=db)
        result = session.execute(select(Pool))
        pools: list[Pool] = result.scalars().all()

    assert pools[0].price > 0


def test_run_token_pool_prices(db):
    with db as session:
        run_token_pool_prices(session=db)
        result = session.execute(select(Token))
        token_pools: list[Token] = result.scalars().all()

    assert token_pools[0].price > 0
