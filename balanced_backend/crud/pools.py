from typing import TYPE_CHECKING
from sqlmodel import select

from balanced_backend.config import settings
from balanced_backend.tables.pools import Pool

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_pools(session: 'Session') -> list[Pool]:
    result = session.execute(select(Pool).where(Pool.chain_id == settings.CHAIN_ID))
    return result.scalars().all()
