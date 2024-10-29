import pytest
from sqlmodel import select

from balanced_backend.tables.pools import Pool
from balanced_backend.tables.tokens import Token
from balanced_backend.tables.stats import Stats
from balanced_backend.cron import (
    pool_prices,
    pool_lists,
    pool_stats,
    token_price,
    token_lists,
    token_stats,
    stats,
)


#
#   NOTE: Tests must be run in order - cron scheduler forces this
#


@pytest.mark.order(1)
def test_run_token_list(db):
    with db as session:
        token_lists.run_token_list(session=session)
        result = session.execute(select(Token))
        tokens = result.scalars().all()

    assert len(tokens) > 30


@pytest.mark.flaky
@pytest.mark.order(1)
def test_run_pool_list(db):
    with db as session:
        pool_lists.run_pool_list(session=session)
        result = session.execute(select(Pool))
        pools = result.scalars().all()

    assert len(pools) > 30


@pytest.mark.flaky
@pytest.mark.order(1)
def test_run_pool_prices(db):
    with db as session:
        pool_prices.run_pool_prices(session=session)
        result = session.execute(select(Pool))
        pools: list[Pool] = result.scalars().all()

    assert pools[0].price > 0


@pytest.mark.flaky(delay=10, retries=3)
@pytest.mark.order(1)
def test_run_token_prices(db):
    with db as session:
        token_price.run_token_prices(session=session)
        result = session.execute(select(Token))
        token_pools: list[Token] = result.scalars().all()

    assert token_pools[0].price > 0


@pytest.mark.order(1)
def test_run_pool_stats(db):
    with db as session:
        pool_stats.run_pool_stats(session=session)
        result = session.execute(select(Pool))
        pools: list[Pool] = result.scalars().all()

    assert pools[0].base_liquidity >= 0


@pytest.mark.order(1)
def test_run_token_stats(db):
    with db as session:
        token_stats.run_token_stats(session=session)
        result = session.execute(select(Token))
        tokens: list[Token] = result.scalars().all()

    assert tokens[0].liquidity >= 0


# TODO: From some reason it doesn't like this?
# @pytest.mark.order(1)
# def test_run_stats(db):
#     with db as session:
#         run_stats = stats.run_balanced_stats(session=session)
#         result = session.execute(select(Stats))
#         stats = result.scalars().all()
