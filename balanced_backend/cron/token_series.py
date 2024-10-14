from typing import TYPE_CHECKING
from loguru import logger

from balanced_backend.addresses import addresses
from balanced_backend.config import settings
from balanced_backend.cron.pool_series import TIME_SERIES_TABLES
from balanced_backend.crud.series import (
    get_last_pool_series_record,
    get_last_token_series_record,
    get_pool_series_table_by_timestamp,
)
from balanced_backend.tables.utils import get_token_series_table, get_pool_series_table
from balanced_backend.utils.rpc import get_band_price
from balanced_backend.utils.prices import PoolPrice, TokenPrice
from balanced_backend.utils.pools import get_cached_pool_stats
from balanced_backend.utils.prices import get_token_prices
from balanced_backend.utils.tokens import get_cached_token_info

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from balanced_backend.cron.pool_series import SeriesTable
    from balanced_backend.tables.utils import PoolSeriesTableType


def calculate_token_prices(
        pool_records: list['PoolSeriesTableType'],
        icx_price: float,
        root_address: str,
        pool_price_type: str,
) -> list[TokenPrice]:
    pools = []
    tokens = []
    for p in pool_records:
        quote_address = get_cached_pool_stats(pool_id=p.pool_id)['quote_address']
        base_address = get_cached_pool_stats(pool_id=p.pool_id)['base_address']

        if quote_address is None and base_address == addresses.SICX_CONTRACT_ADDRESS:
            quote_address = 'ICX'

        pools.append(PoolPrice(
            pool_id=p.pool_id,
            total_supply=p.total_supply,
            quote_address=quote_address,
            base_address=base_address,
            price=getattr(p, pool_price_type),
        ))

        tokens.append(TokenPrice(address=quote_address))
        tokens.append(TokenPrice(address=base_address))

    token_prices = get_token_prices(
        pools=pools,
        tokens=tokens,
        icx_price=icx_price,
        root_address=root_address,
    )

    return token_prices


def get_token_series_min_interval(session: 'Session', pool_series: 'SeriesTable'):
    # Get the tables
    pool_table = get_pool_series_table(pool_series.table_suffix)
    token_table = get_token_series_table(pool_series.table_suffix)

    # Get last records
    last_pool_series = get_last_pool_series_record(session=session, table=pool_table)
    if last_pool_series is None:
        logger.info("Need to have some pool series to build token series...")
        return

    last_token_series = get_last_token_series_record(session=session, table=token_table)
    if last_token_series is None:
        first_pool_series = get_last_pool_series_record(
            session=session,
            table=pool_table,
            first=True,
        )
        token_time = first_pool_series.timestamp
    else:
        # Redo the last interval
        token_time = last_token_series.timestamp - pool_series.delta

    while token_time <= last_pool_series.timestamp + pool_series.delta:
        pool_records = get_pool_series_table_by_timestamp(
            session=session,
            table=pool_table,
            timestamp=token_time,
        )
        block_height = pool_records[0].block_height

        pool_ids = set([i.pool_id for i in pool_records])
        if 1 not in pool_ids:
            icx_price = [i.close for i in pool_records if i.pool_id == 2][0]
            root_address = addresses.SICX_CONTRACT_ADDRESS
        else:
            icx_price = get_band_price(symbol='ICX', height=block_height)
            root_address = 'ICX'

        # A dict to add the results of calculating the prices for different ranges
        # ie price, high, low
        token_price_dict = {}
        for price_type in [
            {
                'pool_column': 'close',
                'token_column': 'price',
            },
            {
                'pool_column': 'high',
                'token_column': 'high',
            },
            {
                'pool_column': 'low',
                'token_column': 'low',
            },
        ]:
            token_prices = calculate_token_prices(
                pool_records=pool_records,
                icx_price=icx_price,
                root_address=root_address,
                pool_price_type=price_type['pool_column'],
            )
            for t in token_prices:
                if t.address not in token_price_dict:
                    token_price_dict[t.address] = {}
                token_price_dict[t.address][price_type['token_column']] = t.price

        for k, v in token_price_dict.items():
            tt = token_table(
                address=k,
                symbol=get_cached_token_info(address=k).symbol,
                chain_id=settings.CHAIN_ID,
                timestamp=token_time,
                block_height=block_height,
                price=v['price'],
                price_low=v['low'],
                price_high=v['high'],
            )
            session.merge(tt)
        session.commit()

        token_time += pool_series.delta


def run_token_series(session: 'Session'):
    logger.info("Running token series cron...")

    # Update each of the tables
    for ts in TIME_SERIES_TABLES:
        get_token_series_min_interval(session=session, pool_series=ts)

    logger.info("Ending token series cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_token_series(session=session)
