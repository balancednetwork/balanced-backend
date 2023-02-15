from typing import TYPE_CHECKING, NewType, Union
from sqlmodel import select
from loguru import logger
import sys
from datetime import datetime

from balanced_backend.tables.dex import DexSwap
from balanced_backend.config import settings
from balanced_backend.tables.volumes import (
    VolumeSeries15Min,
    VolumeSeries1Hour,
    VolumeSeries1Day,
    VolumeSeries30Day,
)
from balanced_backend.utils.time_to_block import get_timestamp_from_block

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


TableType = NewType(
    'TableType',
    Union[
            VolumeSeries15Min,
            VolumeSeries1Hour,
            VolumeSeries1Day,
            VolumeSeries30Day,
        ]
)

TIME_SERIES_TABLES = [
    {
        'name': '15Min',
        'delta': 60 * 15,
    },
    {
        'name': '1Hour',
        'delta': 60 * 60,
    },
    {
        'name': '1Day',
        'delta': 60 * 60 * 24,
    },
    {
        'name': '30Day',
        'delta': 60 * 60 * 24 * 30,
    },
]

def get_table(table_suffix: str) -> TableType:
    Table: TableType = getattr(sys.modules['__main__'], "VolumeSeries" + table_suffix)
    return Table


def get_last_volume_time(session: 'Session', table_suffix: str):
    Table = get_table(table_suffix)
    result = session.execute(select(Table).where(
        Table.chain_id == settings.CHAIN_ID).order_by(Table.block_end.desc()))
    return result.scalars().first()


def get_time_series(
        session: 'Session',
        start_time: int,
        end_time: int
) -> list[DexSwap]:
    result = session.execute(select(DexSwap).where(
        DexSwap.chain_id == settings.CHAIN_ID).where(
        DexSwap.timestamp > start_time).where(
        DexSwap.timestamp <= end_time)
    )
    return result.scalars().all()


def get_start_and_end_times(start_time: int, interval: int) -> list[int]:
    current_time = datetime.now().timestamp()
    time_diff = current_time - start_time
    time_ranges = [
        i * interval + start_time for i in range(0, int(time_diff / interval))
    ]
    return time_ranges


def run_pool_volumes_series(session: 'Session'):
    logger.info("Running pool volumes cron...")

    if settings.FIRST_BLOCK_TIMESTAMP is None:
        settings.FIRST_BLOCK_TIMESTAMP = get_timestamp_from_block(
            block=settings.FIRST_BLOCK
        )

    for i in TIME_SERIES_TABLES:
        last_volume_time = get_last_volume_time(session=session, table_suffix=i['name'])
        if last_volume_time is None:
            last_volume_time = settings.FIRST_BLOCK_TIMESTAMP

        for t in get_start_and_end_times(last_volume_time, i['interval']):
            volume = get_time_series(
                session=session, start_time=t, end_time=t + i['interval']
            )
            session.merge(volume)

        session.commit()


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    run_pool_volumes_series(session_factory())
