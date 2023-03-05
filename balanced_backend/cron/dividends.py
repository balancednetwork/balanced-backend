from typing import TYPE_CHECKING
from sqlmodel import select
from loguru import logger
from pydantic import BaseModel
from datetime import datetime

from balanced_backend.db import session_factory
from balanced_backend.tables.dex import DexSwap
from balanced_backend.tables.dividends import Dividend
from balanced_backend.tables.utils import get_pool_series_table
from balanced_backend.config import settings
from balanced_backend.utils.time_to_block import get_timestamp_from_block

from balanced_backend.crud.dex import get_dex_swaps
from balanced_backend.crud.pools import get_pools

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class DividendPeriod(BaseModel):
    period: str
    delta: int


PERIODS: list[DividendPeriod] = [
    DividendPeriod(
        period="",
        delta=60,
    )
]


def run_pool_dividends(session: 'Session'):
    """
    Cron to calculate the dividends produced from each pool on a token basis. Dividends
     are produced by `Swap` events from the dex as both baln and lp fees. We need to
     take these events and summarize them over the last 24h and 30d volumes. Only the
     swaps within a pool from the `from_address` are allocated to a token. While we are
     doing this we also are going to build volumes as we're already parsing these
     events. Can't do this until all the swaps have been updated in the DB through the
     contracts/dex_swaps.py cron job.
    """
    logger.info("Running pool dividends cron cron...")

    current_timestamp = int(datetime.now().timestamp())
    pools = get_pools(session=session)

    for p in pools:
        swaps = get_dex_swaps(
            session=session,
            start_time=current_timestamp - 86400 * 30,
            pool_id=p.pool_id
        )
        dividend = Dividend(
            chain_id=settings.CHAIN_ID,
            pool_id=p.pool_id,
            base_address=p.base_address,
            quote_address=p.quote_address,
        )
        time_24h_ago = current_timestamp - 86400

        dividend.base_volume_24h = sum(
            [i.base_token_value_decimal for i in swaps if
             i.timestamp > time_24h_ago and i.base_token == p.base_address]
        )
        dividend.quote_volume_24h = sum(
            [i.quote_token_value_decimal for i in swaps if
             i.timestamp > time_24h_ago and i.base_token == p.quote_address]
        )
        dividend.base_volume_30d = sum(
            [i.base_token_value_decimal for i in swaps if
             i.base_token == p.base_address]
        )
        dividend.quote_volume_30d = sum(
            [i.quote_token_value_decimal for i in swaps if
             i.base_token == p.quote_address]
        )
        dividend.base_lp_fees_24h = sum(
            [i.lp_fees_decimal for i in swaps if
             i.timestamp > time_24h_ago and i.from_token == p.base_address]
        )
        dividend.quote_lp_fees_24h = sum(
            [i.lp_fees_decimal for i in swaps if
             i.timestamp > time_24h_ago and i.from_token == p.quote_address]
        )
        dividend.base_lp_fees_30d = sum(
            [i.lp_fees_decimal for i in swaps if i.from_token == p.base_address]
        )
        dividend.quote_lp_fees_30d = sum(
            [i.lp_fees_decimal for i in swaps if i.from_token == p.quote_address]
        )
        dividend.base_baln_fees_24h = sum(
            [i.baln_fees_decimal for i in swaps if
             i.timestamp > time_24h_ago and i.from_token == p.base_address]
        )
        dividend.quote_baln_fees_24h = sum(
            [i.baln_fees_decimal for i in swaps if
             i.timestamp > time_24h_ago and i.from_token == p.quote_address]
        )
        dividend.base_baln_fees_30d = sum(
            [i.baln_fees_decimal for i in swaps if i.from_token == p.base_address]
        )
        dividend.quote_baln_fees_30d = sum(
            [i.baln_fees_decimal for i in swaps if i.from_token == p.quote_address]
        )

        session.merge(dividend)
        session.commit()


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    run_pool_dividends(session_factory())
