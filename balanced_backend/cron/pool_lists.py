from sqlmodel import select
from datetime import datetime
from loguru import logger

from balanced_backend.config import settings
from balanced_backend.tables.pools import Pool
from balanced_backend.tables.tokens import Token
from balanced_backend.addresses import addresses
from balanced_backend.utils.rpc import (
    get_contract_method_int,
    get_contract_method_str,
    get_pool_stats,
)

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_pools() -> list[dict]:
    pool_nonce: int = get_contract_method_int(
        to_address=addresses.DEX_CONTRACT_ADDRESS,
        method='getNonce'
    )

    pool_stats: list[Optional[dict]] = []
    for i in range(1, pool_nonce):
        ps = get_pool_stats(i)
        ps['poolId'] = i
        pool_stats.append(ps)

    return pool_stats


def get_pool_type(tokens: list[Token], quote_symbol: str, base_symbol: str):
    pool_types = [
        i.type for i in tokens if i.symbol == quote_symbol or i.symbol == base_symbol
    ]
    if 'community' in pool_types:
        return 'community'
    return 'balanced'


def run_pool_list(
        session: 'Session',
):
    logger.info("Running pool lists cron...")
    result = session.execute(select(Pool).where(Pool.chain_id == settings.CHAIN_ID))
    pools = result.scalars().all()
    pool_names_db = [i.name for i in pools]

    current_timestamp = int(datetime.now().timestamp())

    result = session.execute(select(Token).where(Token.chain_id == settings.CHAIN_ID))
    tokens = result.scalars().all()

    pool_stats = get_pools()

    for ps in pool_stats:
        if ps['name'] in pool_names_db:
            # We already have pool in DB -> this assumes pool names don't change
            # If they do / if the pool_id changes -> clear pools table and re-init
            continue

        if ps['quote_token'] is not None:
            quote_name = get_contract_method_str(
                to_address=ps['quote_token'],
                method='name'
            )
            quote_symbol = get_contract_method_str(
                to_address=ps['quote_token'],
                method='symbol'
            )
            quote_address = ps['quote_token']
        else:
            quote_symbol = 'ICX'
            quote_address = 'ICX'
            quote_name = 'ICON'

        base_name = get_contract_method_str(
            to_address=ps['base_token'],
            method='name'
        )
        base_symbol = get_contract_method_str(
            to_address=ps['base_token'],
            method='symbol'
        )

        base_address = ps['base_token']

        pool_type = get_pool_type(
            tokens=tokens,
            quote_symbol=quote_symbol,
            base_symbol=base_symbol
        )

        pool_db = Pool(
            base_address=base_address,
            quote_address=quote_address,
            pool_id=ps['poolId'],
            name=f"{base_symbol}/{quote_symbol}",
            base_name=base_name,
            quote_name=quote_name,
            base_symbol=base_symbol,
            quote_symbol=quote_symbol,
            base_decimals=int(ps['base_decimals'], 16),
            quote_decimals=int(ps['quote_decimals'], 16),
            chain_id=settings.CHAIN_ID,
            type=pool_type,
            last_updated_timestamp=current_timestamp,
        )
        session.merge(pool_db)
        session.commit()
    logger.info("Ending pool lists cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_pool_list(session=session)
