from typing import TYPE_CHECKING
from loguru import logger

from balanced_backend.crud.pools import get_pools
from balanced_backend.crud.tokens import get_tokens
from balanced_backend.utils.prices import PoolPrice, TokenPrice, get_token_prices
from balanced_backend.utils.time_to_block import get_block_from_timestamp
from balanced_backend.utils.rpc import get_band_price

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from balanced_backend.tables.pools import Pool

PERIOD_TIMES = {
    '24h': 60 * 60 * 24,
    '7d': 60 * 60 * 24 * 7,
    '30d': 60 * 60 * 24 * 30,
}


def set_previous_prices(
        session: 'Session',
        pools: list['Pool'],
        period: str,
):
    pool_prices = []
    # 7d
    for p in pools:
        pool_prices.append(PoolPrice(
            pool_id=p.pool_id,
            base_address=p.base_address,
            quote_address=p.quote_address,
            total_supply=p.total_supply,
            price=getattr(p, f"price_{period}")
        ))
    block_height = get_block_from_timestamp(
        timestamp=int((pools[0].last_updated_timestamp - PERIOD_TIMES[period]) * 1e6)
    )
    icx_price = get_band_price(symbol='ICX', height=block_height)

    tokens = get_tokens(session=session)
    token_prices = [TokenPrice(**i.dict()) for i in tokens]
    token_prices = get_token_prices(
        pools=pool_prices,
        tokens=token_prices,
        icx_price=icx_price,
    )
    for t in tokens:
        price = [i.price for i in token_prices if i.address == t.address][0]
        setattr(t, f"price_{period}", price)
        session.merge(t)
    session.commit()


def run_token_prices(session: 'Session'):
    logger.info("Running token prices cron...")
    pools = get_pools(session=session)
    tokens = get_tokens(session=session)

    # Current
    pool_prices = [PoolPrice(**i.dict()) for i in pools]
    token_prices = [TokenPrice(**i.dict()) for i in tokens]
    token_prices = get_token_prices(pools=pool_prices, tokens=token_prices)
    for t in tokens:
        t.price = [i.price for i in token_prices if i.address == t.address][0]
        t.path = [i.path for i in token_prices if i.address == t.address][0]
        session.merge(t)
    session.commit()

    for period in ['24h', '7d', '30d']:
        set_previous_prices(session=session, pools=pools, period=period)

    logger.info("Ending token prices cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_token_prices(session=session)
