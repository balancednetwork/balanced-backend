from typing import TYPE_CHECKING
from sqlmodel import select
from datetime import datetime
import networkx as nx

from pydantic import BaseModel

from balanced_backend.config import settings
from balanced_backend.tables.tokens import Token, TokenPrice
from balanced_backend.tables.pools import Pool
from balanced_backend.utils.rpc import get_band_price
from balanced_backend.utils.time_to_block import get_block_from_timestamp

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class TokenPrice(BaseModel):
    name: str
    address: str
    price: float
    pool_id: int
    # TODO: rm None
    total_supply: float = None


def get_pools_with_token(token_address: str, pools: list[Pool]) -> list[Pool]:
    token_pools: list[Pool] = [
        i for i in pools
        if i.base_address == token_address or i.quote_address == token_address
    ]
    return token_pools


def get_pools_with_token_index(token_address: str, pools: list[Pool]) -> list[Pool]:
    token_pools: list[Pool] = [
        pools.pop(i) for i, v in enumerate(pools)
        if v.base_address == token_address or v.quote_address == token_address
    ]
    return token_pools


def get_price_given_ref(pool: Pool, reference_price: float, reference_type: str):
    if reference_type == 'base':
        price = pool.price * reference_price
        return price
    price = pool.price / reference_price
    return price


def get_prices(
        token_prices: list[TokenPrice],
        pools: list[Pool],
        input_address: str,
        input_price: float,
):
    if len(pools) == 0:
        return token_prices

    target_pools = get_pools_with_token_index(
        token_address=input_address,
        pools=pools,
    ).copy()

    for p in target_pools:
        if p.base_address == input_address:
            known_name = p.quote_name
            known_price = input_price / p.price
            known_address = p.quote_address
        else:
            known_name = p.base_name
            known_price = p.price * input_price
            known_address = p.base_address

        print()

        # Store output
        token_prices.append(TokenPrice(
            name=known_name,
            address=known_address,
            price=known_price,
            pool_id=p.pool_id
        ))

        # Recurse to find
        get_prices(
            token_prices=token_prices,
            pools=pools,
            input_address=known_address,
            input_price=known_price,
        )
    return token_prices


def run_token_prices(session: 'Session'):
    result = session.execute(select(Pool).where(Pool.chain_id == settings.CHAIN_ID))
    pools: list[Pool] = result.scalars().all()

    # Output is stored here then we take weighted average at the end
    token_prices: list[TokenPrice] = []

    # Need to seed our
    icx_price = get_band_price(symbol='ICX')

    token_prices = get_prices(
        token_prices=token_prices,
        pools=pools,
        input_address='ICX',
        input_price=icx_price,
    )
    print()

    # Get the index of the ICX pools from all pools in DB (note: not the pool ID)
    # Should be only one pool.
    # icx_pool_indexes = [i for i, v in enumerate(pools) if v.quote_address == 'ICX']
    # reference_pools: list[Pool] = []
    #
    # for i, _ in enumerate(icx_pool_indexes):
    #     reference_pools.append(pools.pop(i))
    #
    # for p in reference_pools:
    #     if p.base_address == 'ICX':
    #         # This might not ever be called
    #         token_prices.append(TokenPrice(
    #             address=p.quote_address,
    #             price=p.price * icx_price,
    #             pool_id=p.pool_id
    #         ))
    #     else:
    #         token_prices.append(TokenPrice(
    #             address=p.base_address,
    #             price=p.price / icx_price,
    #             pool_id=p.pool_id
    #         ))
    #
    # while len(pools) > 0:
    #     token_pools = get_pools_with_token(token_address='ICX', pools=pools)
    #     print()
    # # for tp in token_pools:
    # #     if tp.base_address == :
    # #         price = tp.price * reference_price
    # #     else:
    # #         price = tp.price / reference_price
    # #
    # #     price = get_price_given_ref(pool=tp, reference_price=icx_price, reference_type='base')
    # #     token_prices.append({'name': })
    # #
    # #     print()
    #
    # for p in pools:
    #     if p.quote_address == 'ICX':
    #         print()
    #     else:
    #         print()
    #
    # print()


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    run_token_prices(session_factory())
