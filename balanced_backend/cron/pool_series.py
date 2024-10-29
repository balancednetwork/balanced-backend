from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import delete
from sqlmodel import select
from loguru import logger
from pydantic import BaseModel
import asyncio

from balanced_backend.crud.dex import get_dex_swaps, get_last_swap_time
from balanced_backend.crud.series import get_pool_series_table_by_timestamp
from balanced_backend.tables.dex import DexSwap
from balanced_backend.tables.series import PoolSeriesTableType
from balanced_backend.tables.utils import get_pool_series_table
from balanced_backend.config import settings
from balanced_backend.utils.pools import get_cached_pool_stats
from balanced_backend.utils.time_to_block import (
    get_timestamp_from_block,
    get_block_from_timestamp,
)
from balanced_backend.utils.rpc_async import get_total_supply_async

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class SeriesTable(BaseModel):
    table_suffix: str
    delta: int
    pool_ids: set[int] = set()
    pool_close: dict[int, float] = {}
    skip_modulo: int = 1  # Do run_number % skip_modulo == 0 for skipping long updates


TIME_SERIES_TABLES: list[SeriesTable] = [
    # SeriesTable(
    #     table_suffix="5Min",
    #     delta=60 * 5,
    # ),
    # SeriesTable(
    #     table_suffix="15Min",
    #     delta=60 * 15,
    # ),
    # SeriesTable(
    #     table_suffix="1Hour",
    #     delta=60 * 60,
    # ),
    # SeriesTable(
    #     table_suffix="4Hour",
    #     delta=60 * 60 * 4,
    # ),
    # SeriesTable(
    #     table_suffix="1Day",
    #     delta=60 * 60 * 24,
    # ),
    SeriesTable(
        table_suffix="1Week",
        delta=60 * 60 * 24 * 7,
        skip_modulo=10,
    ),
    # SeriesTable(
    #     table_suffix="1Month",
    #     delta=60 * 60 * 24 * 30,
    # ),
]


def get_last_volume_time(session: 'Session', table: PoolSeriesTableType) -> int:
    result = session.execute(select(table).where(
        table.chain_id == settings.CHAIN_ID
    ).order_by(table.timestamp.desc()).limit(1).limit(1))
    last_volume = result.scalars().first()
    if last_volume is None:
        volume_time = int(get_timestamp_from_block(block=settings.FIRST_BLOCK) / 1e6)
    else:
        volume_time = last_volume.timestamp
    return volume_time


RUN_NUMBER_COUNT_DICT: dict[int, int] = {}


def _skip_time_series(pool_volume: SeriesTable) -> bool:
    if pool_volume.delta not in RUN_NUMBER_COUNT_DICT:
        RUN_NUMBER_COUNT_DICT[pool_volume.delta] = 0

    RUN_NUMBER_COUNT_DICT[pool_volume.delta] += 1
    run_count = RUN_NUMBER_COUNT_DICT[pool_volume.delta]

    if not run_count - 1 % pool_volume.skip_modulo == 0:
        return True
    return False


def get_time_series_for_interval(session: 'Session', pool_volume: SeriesTable):
    # Get the table we want to be building the series dynamically since there are many
    if _skip_time_series(pool_volume):
        return

    Table = get_pool_series_table(table_suffix=pool_volume.table_suffix)

    logger.info(f"Running series {pool_volume.table_suffix}...")

    # Get the last swap in the dex swap table so we know where to iterate up to
    last_swap = get_last_swap_time(session=session)
    if last_swap is None:
        logger.info("No swaps in DB, returning until those have been filled in...")
        return
    else:
        last_swap_time = last_swap.timestamp

    # Get the last time in the volume table minus delta so we rebuild the last period
    volume_time = get_last_volume_time(
        session=session,
        table=Table,
    ) - pool_volume.delta

    # Get the last time series so we know when to index from
    last_volume_timeseries = get_pool_series_table_by_timestamp(
        session=session,
        table=Table,
        timestamp=int(volume_time),
    )
    if len(last_volume_timeseries) != 0:
        pool_volume.pool_ids = set([i.pool_id for i in last_volume_timeseries])

    # Initialize with the last known pool price. Otherwise this is done in the loop
    for p in pool_volume.pool_ids:
        pool_series = [i for i in last_volume_timeseries if i.pool_id == p][0]
        pool_volume.pool_close[p] = pool_series.open

    current_time = datetime.now().timestamp()
    head = False
    while volume_time < last_swap_time + pool_volume.delta:

        if volume_time > current_time:
            head = True
            volume_time = datetime.now().timestamp()

        swaps = get_dex_swaps(
            session=session,
            start_time=volume_time - pool_volume.delta,
            end_time=volume_time,
            columns=[
                DexSwap.pool_id,
                DexSwap.ending_price_decimal,
                DexSwap.base_token_value_decimal,
                DexSwap.quote_token_value_decimal,
                DexSwap.lp_fees_decimal,
                DexSwap.baln_fees_decimal,
            ]
        )

        # Need extra call here because there may be no swaps in a period. This is needed
        # because we need to enrich this series with pool stats data to later be able to
        # calculate the token prices.
        block_height = get_block_from_timestamp(
            int((volume_time + pool_volume.delta / 2) * 1e6))
        # TODO: To make this faster we can check if there are no swaps and if there
        #  aren't, then estimate the BH, skip the total supply call by carrying over the
        #  last total supply. This is definitely slow but might be faster in cluster.

        logger.info(f"Summarizing num swaps: {len(swaps)} at bh: {block_height} in "
                    f"segment: {pool_volume.table_suffix}...")

        # Add any new pool IDs that need to be tracked
        new_pool_ids = set([
            i.pool_id for i in swaps if i.pool_id not in pool_volume.pool_ids
        ])

        for np in new_pool_ids:
            pool_volume.pool_ids.add(np)
            pool_volume.pool_close[np] = 0

        # TODO: To make this faster, we can update the total supplies every X number of
        #  iterations as this is only used to do the price path search
        total_supplies = asyncio.run(
            get_total_supply_async(
                pool_ids=list(pool_volume.pool_ids),
                height=block_height,
            )
        )

        for p in pool_volume.pool_ids:
            # if settings.VERBOSE:
            logger.info(
                f"Processing pool: {p} in segment: {pool_volume.table_suffix}...")

            if head:
                query = delete(Table).where(Table.head).where(Table.pool_id == p)
                session.execute(query)
                volume_time = datetime.now().timestamp()

            total_supply = [i for i in total_supplies if i['pool_id'] == p][0][
                'total_supply']

            pool_swaps = [i for i in swaps if i.pool_id == p]
            swap_prices = [i.ending_price_decimal for i in pool_swaps]
            if len(swap_prices) != 0:
                high = max(swap_prices)
                low = min(swap_prices)
                close = swap_prices[-1]
            else:
                high = pool_volume.pool_close[p]
                low = pool_volume.pool_close[p]
                close = pool_volume.pool_close[p]

            open = pool_volume.pool_close[p]
            pool_volume.pool_close[p] = close

            # Old API just assumed base here
            base_volume = sum([i.base_token_value_decimal for i in pool_swaps])
            quote_volume = sum([i.quote_token_value_decimal for i in pool_swaps])

            # Fees
            quote_lp_fees = sum([
                i.lp_fees_decimal for i in pool_swaps
                if i.from_token == get_cached_pool_stats(pool_id=p)['quote_address']
            ])
            quote_baln_fees = sum([
                i.baln_fees_decimal for i in pool_swaps
                if i.from_token == get_cached_pool_stats(pool_id=p)['quote_address']
            ])
            base_lp_fees = sum([
                i.lp_fees_decimal for i in pool_swaps
                if i.from_token == get_cached_pool_stats(pool_id=p)['base_address']
            ])
            bases_baln_fees = sum([
                i.baln_fees_decimal for i in pool_swaps
                if i.from_token == get_cached_pool_stats(pool_id=p)['base_address']
            ])

            t = Table(
                chain_id=settings.CHAIN_ID,
                pool_id=p,
                timestamp=volume_time,
                block_height=block_height,
                high=high,
                low=low,
                open=open,
                close=close,
                base_volume=base_volume,
                quote_volume=quote_volume,
                quote_lp_fees=quote_lp_fees,
                quote_baln_fees=quote_baln_fees,
                base_lp_fees=base_lp_fees,
                base_baln_fees=bases_baln_fees,
                total_supply=total_supply,
                head=head,
            )

            session.merge(t)
            # We have a memory issue that this seemed to fix
            # if num_swaps > 10000:
            session.commit()
        # if num_swaps <= 10000:
        #     session.commit()
        volume_time = volume_time + pool_volume.delta


def run_pool_volumes_series(session: 'Session'):
    logger.info("Running pool volumes cron...")

    # Update each of the tables
    for ts in TIME_SERIES_TABLES:
        get_time_series_for_interval(session=session, pool_volume=ts)
    logger.info("Ending pool volumes cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_pool_volumes_series(session=session)
