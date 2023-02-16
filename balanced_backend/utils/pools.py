from typing import Union
from balanced_backend.utils.rpc import get_pool_id, get_pool_stats

POOL_IDS: dict[str, int] = {}
POOL_DECIMALS: dict[int, dict[str, int]] = {}


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


def get_cached_pool_decimals(pool_id: int) -> dict[str, Union[int, str]]:
    """
    Will error if the pool does not exist. These should be immutable over the span of
     the chain.
    """
    try:
        return POOL_DECIMALS[pool_id]
    except KeyError:
        pool_stats = get_pool_stats(pool_id=pool_id)

        base_decimals = int(pool_stats['base_decimals'], 16)
        quote_decimals = int(pool_stats['quote_decimals'], 16)

        POOL_DECIMALS[pool_id] = {
            'base_address': pool_stats['base_token'],
            'quote_address': pool_stats['quote_token'],
            'base_decimals': base_decimals,
            'quote_decimals': quote_decimals,
            'pool_decimals': 18 + quote_decimals - base_decimals,
        }

        return POOL_DECIMALS[pool_id]
