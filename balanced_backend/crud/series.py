from typing import TYPE_CHECKING
from sqlmodel import select

from balanced_backend.config import settings
from balanced_backend.tables.series import PoolSeriesTableType, TokenSeriesTableType
from balanced_backend.utils.time_to_block import get_timestamp_from_block

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_last_pool_series_record(
        session: 'Session',
        table: PoolSeriesTableType,
        first: bool = False,
) -> PoolSeriesTableType:
    query = select(table).where(
        table.chain_id == settings.CHAIN_ID
    ).limit(1)
    if first:
        query = query.order_by(table.timestamp.asc())
    else:
        query = query.order_by(table.timestamp.desc())
    result = session.execute(query)
    return result.scalars().first()


def get_last_pool_series_time(session: 'Session', table: PoolSeriesTableType) -> int:
    last_volume = get_last_pool_series_record(session, table)
    if last_volume is None:
        volume_time = int(get_timestamp_from_block(block=settings.FIRST_BLOCK) / 1e6)
    else:
        volume_time = last_volume.timestamp
    return volume_time


def get_pool_series_table_by_timestamp(
        session: 'Session',
        table: PoolSeriesTableType,
        timestamp: int,
) -> list[PoolSeriesTableType]:
    result = session.execute(select(table).where(
        table.chain_id == settings.CHAIN_ID,
        table.timestamp == timestamp,
    ).order_by(table.timestamp.desc()))
    return result.scalars().all()


def get_token_series_table_by_timestamp(
        session: 'Session',
        table: TokenSeriesTableType,
        timestamp: int,
) -> list[TokenSeriesTableType]:
    result = session.execute(select(table).where(
        table.chain_id == settings.CHAIN_ID,
        table.timestamp == timestamp,
    ).order_by(table.timestamp.desc()))
    return result.scalars().all()


def get_token_series_table_between_timestamps(
        session: 'Session',
        table: TokenSeriesTableType,
        start_time: int,
        end_time: int,
) -> list[TokenSeriesTableType]:
    result = session.execute(select(table).where(
        table.chain_id == settings.CHAIN_ID,
        table.timestamp >= start_time,
        table.timestamp <= end_time,
    ).order_by(table.timestamp.desc()))
    return result.scalars().all()


def get_last_token_series_record(
        session: 'Session',
        table: TokenSeriesTableType,
) -> TokenSeriesTableType:
    query = select(table).where(
        table.chain_id == settings.CHAIN_ID,
    ).limit(1).order_by(table.timestamp.desc())
    result = session.execute(query)
    return result.scalars().first()
