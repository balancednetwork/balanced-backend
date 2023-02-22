from sqlalchemy.orm import Session
from sqlmodel import select

from balanced_backend.config import settings
from balanced_backend.tables.pools import Pool


def get_pools(session: 'Session') -> list[Pool]:
    result = session.execute(select(Pool).where(Pool.chain_id == settings.CHAIN_ID))
    return result.scalars().all()
