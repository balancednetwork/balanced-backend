from typing import TYPE_CHECKING
from sqlmodel import select
from loguru import logger
from pydantic import BaseModel

from balanced_backend.crud.dex import get_swaps_within_times
from balanced_backend.tables.dex import DexSwap
from balanced_backend.tables.volumes import VolumeTableType
from balanced_backend.tables.utils import get_table
from balanced_backend.config import settings
from balanced_backend.utils.time_to_block import get_timestamp_from_block

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class PoolVolume(BaseModel):
    table_suffix: str
    delta: int
    pool_ids: set[int] = set()
    pool_close: dict[int, float] = {}


TIME_SERIES_TABLES: list[PoolVolume] = [
    PoolVolume(
        table_suffix="5Min",
        delta=60 * 5,
    ),
    PoolVolume(
        table_suffix="15Min",
        delta=60 * 15,
    ),
    PoolVolume(
        table_suffix="1Hour",
        delta=60 * 60,
    ),
    PoolVolume(
        table_suffix="4Hour",
        delta=60 * 60 * 4,
    ),
    PoolVolume(
        table_suffix="1Day",
        delta=60 * 60 * 24,
    ),
    PoolVolume(
        table_suffix="1Week",
        delta=60 * 60 * 24 * 7,
    ),
    PoolVolume(
        table_suffix="1Month",
        delta=60 * 60 * 24 * 30,
    ),
]


def get_last_volume_time(session: 'Session', table: VolumeTableType) -> int:
    result = session.execute(select(table).where(
        table.chain_id == settings.CHAIN_ID
    ).order_by(table.timestamp.desc()))
    last_volume = result.scalars().first()
    if last_volume is None:
        volume_time = int(get_timestamp_from_block(block=settings.FIRST_BLOCK) / 1e6)
    else:
        volume_time = last_volume.timestamp
    return volume_time


def get_last_volume_timeseries(
        session: 'Session',
        table: VolumeTableType,
        timestamp: int,
) -> list[VolumeTableType]:
    result = session.execute(select(table).where(
        table.chain_id == settings.CHAIN_ID,
        table.timestamp == timestamp,
    ))
    return result.scalars().all()


def get_last_swap_time(session: 'Session') -> DexSwap:
    result = session.execute(select(DexSwap).where(
        DexSwap.chain_id == settings.CHAIN_ID
    ).order_by(DexSwap.timestamp.desc()))
    last_swap = result.scalars().first()
    return last_swap


def get_time_series_for_interval(session: 'Session', pool_volume: PoolVolume):
    # Get the table we want to be building the series dynamically since there are many
    Table = get_table(table_suffix=pool_volume.table_suffix)

    # Get the last swap in the dex swap table so we know where to iterate up to
    last_swap = get_last_swap_time(session=session)
    if last_swap is None:
        logger.info("No swaps in DB, returning until those have been filled in...")
        return
    else:
        last_swap_time = last_swap.timestamp

    # Get the last time in the volume table minus delta to we rebuild the last period
    volume_time = get_last_volume_time(
        session=session,
        table=Table,
    ) - pool_volume.delta

    # Get the last time series so we know when to index from
    last_volume_timeseries = get_last_volume_timeseries(
        session=session,
        table=Table,
        timestamp=int(volume_time),
    )
    if len(last_volume_timeseries) != 0:
        pool_volume.pool_ids = set([i.pool_id for i in last_volume_timeseries])

    # Initialize with the last known pool price. Otherwise this is done in the loop
    for p in pool_volume.pool_ids:
        pool_series = [i for i in last_volume_timeseries if i.pool_id == p][0]
        pool_volume.pool_close[p] = pool_series.close

    while volume_time < last_swap_time:
        swaps = get_swaps_within_times(
            session=session,
            start_time=volume_time,
            end_time=volume_time + pool_volume.delta
        )

        # Add any new pool IDs that need to be tracked
        new_pool_ids = set([
            i.pool_id for i in swaps if i.pool_id not in pool_volume.pool_ids
        ])

        for np in new_pool_ids:
            pool_volume.pool_ids.add(np)
            pool_volume.pool_close[np] = 0

        for p in pool_volume.pool_ids:
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
            lp_fees = sum([i.lp_fees_decimal for i in pool_swaps])
            baln_fees = sum([i.baln_fees_decimal for i in pool_swaps])

            t = Table(
                chain_id=settings.CHAIN_ID,
                pool_id=p,
                timestamp=volume_time,
                high=high,
                low=low,
                open=open,
                close=close,
                base_volume=base_volume,
                quote_volume=quote_volume,
                lp_fees=lp_fees,
                baln_fees=baln_fees,
            )
            session.merge(t)

            session.commit()
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
