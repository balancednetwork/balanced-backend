from typing import TYPE_CHECKING
from sqlmodel import select
from loguru import logger

from balanced_backend.config import settings
from balanced_backend.tables.dex import DexAdd
from balanced_backend.utils.rpc import get_last_block
from balanced_backend.utils.dex import get_dex_adds

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_dex_adds_in_range(
        session: 'Session',
        start_block: int = None,
        end_block: int = None,
):
    chunks = int((end_block - start_block) / settings.BLOCK_SYNC_CHUNK)

    for i in range(0, chunks):
        block_start = start_block + i * settings.BLOCK_SYNC_CHUNK
        block_end = start_block + (i + 1) * settings.BLOCK_SYNC_CHUNK
        adds = get_dex_adds(block_start=block_start, block_end=block_end)

        for a in adds:
            session.merge(a)
        session.commit()


def get_last_add(session: 'Session') -> DexAdd:
    result = session.execute(select(DexAdd).where(
        DexAdd.chain_id == settings.CHAIN_ID
    ).order_by(DexAdd.block_number.desc()).limit(1))
    return result.scalars().first()


def run_dex_adds(session: 'Session'):
    logger.info("Running dex add cron...")

    last_add = get_last_add(session=session)

    if last_add is None:
        start_block = settings.FIRST_BLOCK
    else:
        start_block = last_add.block_number

    get_dex_adds_in_range(
        session=session,
        start_block=start_block,
        end_block=get_last_block(),
    )
    logger.info("Ending dex add cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_dex_adds(session=session)
