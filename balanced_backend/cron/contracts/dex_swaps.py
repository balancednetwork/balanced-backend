from typing import TYPE_CHECKING
from sqlmodel import select
from loguru import logger

from balanced_backend.config import settings
from balanced_backend.tables.dex import DexSwap
from balanced_backend.utils.rpc import get_last_block
from balanced_backend.utils.volumes import get_swaps

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_dex_swaps_in_range(
        session: 'Session',
        start_block: int = None,
        end_block: int = None,
):
    chunks = int((end_block - start_block) / settings.BLOCK_SYNC_CHUNK)

    for i in range(0, chunks):
        block_start = start_block + i * settings.BLOCK_SYNC_CHUNK
        block_end = start_block + (i + 1) * settings.BLOCK_SYNC_CHUNK
        swaps = get_swaps(block_start=block_start, block_end=block_end)

        for s in swaps:
            session.merge(s)
            session.commit()


def get_last_swap(session: 'Session') -> DexSwap:
    result = session.execute(select(DexSwap).where(
        DexSwap.chain_id == settings.CHAIN_ID
    ).order_by(DexSwap.block_number.desc()).limit(1))
    return result.scalars().first()


def run_dex_swaps(session: 'Session'):
    logger.info("Running dex swap cron...")

    last_swap = get_last_swap(session=session)

    if last_swap is None:
        start_block = settings.FIRST_BLOCK
    else:
        start_block = last_swap.block_number

    get_dex_swaps_in_range(
        session=session,
        start_block=start_block,
        end_block=get_last_block(),
    )
    logger.info("Ending dex swap cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_dex_swaps(session=session)
