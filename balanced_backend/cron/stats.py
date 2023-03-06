from typing import TYPE_CHECKING
from loguru import logger

from balanced_backend.tables.stats import Stats
from balanced_backend.config import settings
from balanced_backend.crud.pools import get_pools

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def run_balanced_stats(session: 'Session'):
    logger.info("Running balanced stats cron...")

    pools = get_pools(session=session)

    fees_earned_24h = sum([
        i.base_price * i.base_lp_fees_24h + i.quote_price * i.quote_lp_fees_24h
        for i in pools
    ])
    fees_earned_30d = sum([
        i.base_price * i.base_lp_fees_30d + i.quote_price * i.quote_lp_fees_30d
        for i in pools
    ])

    stats = Stats(
        chain_id=settings.CHAIN_ID,
        fees_earned_24h=fees_earned_24h,
        fees_earned_30d=fees_earned_30d,
    )
    session.merge(stats)
    session.commit()
    logger.info("Ending balanced stats cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_balanced_stats(session=session)
