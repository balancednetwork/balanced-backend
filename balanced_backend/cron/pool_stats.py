from datetime import datetime
from typing import TYPE_CHECKING
from loguru import logger

from balanced_backend.crud.pools import get_pools
from balanced_backend.crud.tokens import get_tokens
from balanced_backend.crud.dex import get_dex_swaps

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def run_pool_stats(
        session: 'Session',
):
    logger.info("Running pool stats cron...")

    pools = get_pools(session=session)
    tokens = get_tokens(session=session)

    time_24h_ago = int(datetime.now().timestamp() - 86400)
    time_30d_ago = int(datetime.now().timestamp() - 86400 * 30)

    for p in pools:
        swaps = get_dex_swaps(
            session=session,
            start_time=time_24h_ago,
            pool_id=p.pool_id,
        )

        # 24h

        p.base_volume_24h = sum(
            [i.base_token_value_decimal for i in swaps if
             i.timestamp > time_24h_ago and i.base_token == p.base_address]
        )
        p.quote_volume_24h = sum(
            [i.quote_token_value_decimal for i in swaps if
             i.timestamp > time_24h_ago and i.quote_token == p.quote_address]
        )
        p.base_lp_fees_24h = sum(
            [i.lp_fees_decimal for i in swaps if
             i.timestamp > time_24h_ago and i.from_token == p.base_address]
        )
        p.quote_lp_fees_24h = sum(
            [i.lp_fees_decimal for i in swaps if
             i.timestamp > time_24h_ago and i.from_token == p.quote_address]
        )
        p.base_baln_fees_24h = sum(
            [i.baln_fees_decimal for i in swaps if
             i.timestamp > time_24h_ago and i.from_token == p.base_address]
        )
        p.quote_baln_fees_24h = sum(
            [i.baln_fees_decimal for i in swaps if
             i.timestamp > time_24h_ago and i.from_token == p.quote_address]
        )

        # 30d

        swaps = get_dex_swaps(
            session=session,
            start_time=time_30d_ago,
            pool_id=p.pool_id,
        )

        p.base_volume_30d = sum(
            [i.base_token_value_decimal for i in swaps if
             i.timestamp > time_30d_ago and i.base_token == p.base_address]
        )
        p.quote_volume_30d = sum(
            [i.quote_token_value_decimal for i in swaps if
             i.timestamp > time_30d_ago and i.quote_token == p.quote_address]
        )
        p.base_lp_fees_30d = sum(
            [i.lp_fees_decimal for i in swaps if
             i.timestamp > time_30d_ago and i.from_token == p.base_address]
        )
        p.quote_lp_fees_30d = sum(
            [i.lp_fees_decimal for i in swaps if
             i.timestamp > time_30d_ago and i.from_token == p.quote_address]
        )
        p.base_baln_fees_30d = sum(
            [i.baln_fees_decimal for i in swaps if
             i.timestamp > time_30d_ago and i.from_token == p.base_address]
        )
        p.quote_baln_fees_30d = sum(
            [i.baln_fees_decimal for i in swaps if
             i.timestamp > time_30d_ago and i.from_token == p.quote_address]
        )

        p.base_price = [i.price for i in tokens if i.address == p.base_address][0]
        p.quote_price = [i.price for i in tokens if i.address == p.quote_address][0]

        session.merge(p)

    session.commit()

    logger.info("Ending pool stats cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_pool_stats(session=session)
