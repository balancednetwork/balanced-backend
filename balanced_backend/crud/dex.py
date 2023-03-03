from typing import TYPE_CHECKING
from sqlmodel import select

from balanced_backend.config import settings
from balanced_backend.tables.dex import DexSwap

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_dex_swaps(
        session: 'Session',
        start_time: int = None,
        end_time: int = None,
        pool_id: int = None,
        limit: int = None
) -> list[DexSwap]:
    query = select(DexSwap).where(DexSwap.chain_id == settings.CHAIN_ID)

    if start_time is not None:
        query = query.where(DexSwap.timestamp > start_time)
    if end_time is not None:
        query = query.where(DexSwap.timestamp <= end_time)
    if pool_id is not None:
        query = query.where(DexSwap.pool_id == pool_id)
    if limit is not None:
        query = query.limit(limit)

    if limit is not None and (start_time is None and end_time is None):
        query = query.order_by(DexSwap.timestamp.desc())

    result = session.execute(query)
    return result.scalars().all()


def get_last_swap_time(session: 'Session') -> DexSwap:
    result = session.execute(select(DexSwap).where(
        DexSwap.chain_id == settings.CHAIN_ID
    ).order_by(DexSwap.timestamp.desc()).limit(1))
    last_swap = result.scalars().first()
    return last_swap

