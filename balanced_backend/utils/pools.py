from typing import TypedDict
from balanced_backend.utils.rpc import (
    get_pool_id,
    get_pool_stats,
    get_contract_method_str,
)


class PoolStats(TypedDict):
    base_address: str
    quote_address: str
    base_symbol: str
    quote_symbol: str
    base_decimals: int
    quote_decimals: int
    pool_decimals: int


POOL_IDS: dict[str, int] = {}
POOL_STATS: dict[int, PoolStats] = {}

def get_cached_pool_id(base_address: str, quote_address: str) -> int:
    """
    Will error if the pool does not exist. These are immutable over the span of the
     chain.
    """
    try:
        return POOL_IDS[base_address + quote_address]
    except KeyError:
        pool_id = get_pool_id(
            base_address=quote_address,
            quote_address=base_address,
        )
        POOL_IDS[base_address + quote_address] = pool_id
        return pool_id


def get_cached_pool_stats(pool_id: int, height: int = None) -> PoolStats:
    """
    Will error if the pool does not exist. These should be immutable over the span of
     the chain.
    """
    try:
        return POOL_STATS[pool_id]
    except KeyError:
        pool_stats = get_pool_stats(pool_id=pool_id, height=height)

        base_decimals = int(pool_stats['base_decimals'], 16)
        quote_decimals = int(pool_stats['quote_decimals'], 16)

        base_symbol = get_contract_method_str(
            to_address=pool_stats['base_token'],
            method='symbol'
        )
        if pool_stats['quote_token'] is not None:
            quote_symbol = get_contract_method_str(
                to_address=pool_stats['quote_token'],
                method='symbol'
            )
        else:
            quote_symbol = 'ICX'

        POOL_STATS[pool_id] = {
            'base_address': pool_stats['base_token'],
            'quote_address': pool_stats['quote_token'],
            'base_symbol': base_symbol,
            'quote_symbol': quote_symbol,
            'base_decimals': base_decimals,
            'quote_decimals': quote_decimals,
            'pool_decimals': 18 + quote_decimals - base_decimals,
        }

        return POOL_STATS[pool_id]
