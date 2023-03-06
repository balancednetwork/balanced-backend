from sqlmodel import select
from datetime import datetime
from loguru import logger

from balanced_backend.config import settings
from balanced_backend.tables.pools import Pool
from balanced_backend.tables.tokens import Token
from balanced_backend.crud.tokens import get_tokens
from balanced_backend.crud.pools import get_pools
from balanced_backend.addresses import addresses
from balanced_backend.utils.rpc import (
    get_contract_method_int,
    get_contract_method_str,
    get_pool_stats,
)

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_pools_from_stats() -> list[dict]:
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


def run_pool_list(session: 'Session'):
    logger.info("Running pool lists cron...")
    current_timestamp = int(datetime.now().timestamp())

    # Get tokens so we can find out what type of token it is
    tokens = get_tokens(session=session)

    # Iterate up to the nonce to get all the pools
    pool_stats = get_pools_from_stats()

    # Get pools so that if it exists we just update the record
    pools = get_pools(session=session)
    pool_ids = [i.pool_id for i in pools]

    for ps in pool_stats:
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

        total_supply = int(ps['total_supply'], 16)
        price = int(ps['price'], 16) / 10 ** (
            18 + int(ps['quote_decimals'], 16) - int(ps['base_decimals'], 16)
        )

        if ps['pool_id'] not in pool_ids:
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
                total_supply=total_supply,
                price=price,
            )
        else:
            pool_db = [i for i in pools if i.pool_id == ps['pool_id']][0]
            pool_db.base_address = base_address
            pool_db.quote_address = quote_address
            pool_db.pool_id = ps['poolId']
            pool_db.name = f"{base_symbol}/{quote_symbol}"
            pool_db.base_name = base_name
            pool_db.quote_name = quote_name
            pool_db.base_symbol = base_symbol
            pool_db.quote_symbol = quote_symbol
            pool_db.base_decimals = int(ps['base_decimals'], 16)
            pool_db.quote_decimals = int(ps['quote_decimals'], 16)
            pool_db.chain_id = settings.CHAIN_ID
            pool_db.type = pool_type
            pool_db.last_updated_timestamp = current_timestamp
            pool_db.total_supply = total_supply
            pool_db.price = price
        session.merge(pool_db)
    session.commit()
    logger.info("Ending pool lists cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_pool_list(session=session)
