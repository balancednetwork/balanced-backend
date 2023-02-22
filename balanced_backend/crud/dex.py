from sqlalchemy.orm import Session
from sqlmodel import select

from balanced_backend.config import settings
from balanced_backend.tables.dex import DexSwap


def get_swaps_within_times(
        session: 'Session',
        start_time: int,
        end_time: int = None,
        pool_id: int = None,
) -> list[DexSwap]:
    query = select(DexSwap).where(
        DexSwap.chain_id == settings.CHAIN_ID).where(
        DexSwap.timestamp > start_time)

    if end_time is not None:
        query = query.where(DexSwap.timestamp <= end_time)
    if pool_id is not None:
        query = query.where(DexSwap.pool_id == pool_id)

    result = session.execute(query)
    return result.scalars().all()
