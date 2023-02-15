from typing import TYPE_CHECKING
from sqlmodel import select
from pydantic import BaseModel
from loguru import logger

from balanced_backend.config import settings
from balanced_backend.tables.tokens import Token, TokenPool, TokenPrice
from balanced_backend.tables.pools import Pool
from balanced_backend.utils.rpc import get_band_price

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class TokenPrice(BaseModel):
    name: str
    symbol: str
    pool_id: int
    address: str
    price: float
    pool_price: float
    pool_name: str
    reference_name: str
    reference_symbol: str
    reference_price: float
    reference_address: str

    # TODO: rm None
    total_supply: float = None


def pop_pools_with_base_token(token_address: str, pools: list[Pool]) -> list[Pool]:
    token_pools: list[Pool] = [
        pools.pop(i) for i, v in enumerate(pools)
        if v.quote_address == token_address
    ]

    return token_pools


def get_prices_base(
        token_prices: list[TokenPrice],
        pools: list[Pool],
        input_address: str,
        input_price: float,
):
    if len(pools) == 0:
        return token_prices

    target_pools = pop_pools_with_base_token(
        token_address=input_address,
        pools=pools,
    )

    for p in target_pools:
        name = p.base_name
        symbol = p.base_symbol
        price = input_price * p.price
        address = p.base_address
        reference_name = p.quote_name
        reference_symbol = p.quote_symbol
        reference_address = p.quote_address

        # Store output
        token_prices.append(TokenPrice(
            name=name,
            address=address,
            symbol=symbol,
            price=price,
            pool_price=p.price,
            pool_id=p.pool_id,
            pool_name=p.name,
            reference_name=reference_name,
            reference_symbol=reference_symbol,
            reference_price=input_price,
            reference_address=reference_address,
        ))

        print()
        # Recurse to find
        get_prices_quote(
            token_prices=token_prices,
            pools=pools,
            input_address=address,
            input_price=price,
        )

    return token_prices


def pop_pools_with_quote_token(token_address: str, pools: list[Pool]) -> list[Pool]:
    token_pools: list[Pool] = [
        pools.pop(i) for i, v in enumerate(pools)
        if v.quote_address == token_address
    ]

    return token_pools


def get_prices_quote(
        token_prices: list[TokenPrice],
        pools: list[Pool],
        input_address: str,
        input_price: float,
):
    if len(pools) == 0:
        return token_prices

    target_pools = pop_pools_with_quote_token(
        token_address=input_address,
        pools=pools,
    )

    for p in target_pools:
        name = p.quote_name
        symbol = p.quote_symbol
        price = input_price / p.price
        address = p.quote_address
        reference_name = p.base_name
        reference_symbol = p.base_symbol
        reference_address = p.base_address

        # Store output
        token_prices.append(TokenPrice(
            name=name,
            address=address,
            symbol=symbol,
            price=price,
            pool_price=p.price,
            pool_id=p.pool_id,
            pool_name=p.name,
            reference_name=reference_name,
            reference_symbol=reference_symbol,
            reference_price=input_price,
            reference_address=reference_address,
        ))

        print()
        # Recurse to find
        get_prices_base(
            token_prices=token_prices,
            pools=pools,
            input_address=address,
            input_price=price,
        )

    return token_prices


def run_token_prices(session: 'Session'):
    logger.info("Running token prices cron...")

    result = session.execute(select(Pool).where(Pool.chain_id == settings.CHAIN_ID))
    pools: list[Pool] = result.scalars().all()
    update_timestamp = pools[0].last_updated_timestamp

    # Output is stored here then we take weighted average at the end
    token_prices: list[TokenPrice] = []

    # Need to seed our
    icx_price = get_band_price(symbol='ICX')

    token_prices = get_prices_base(
        token_prices=token_prices,
        pools=pools,
        input_address='ICX',
        input_price=icx_price,
    )

    for tp in token_prices:
        token_pool_price = TokenPool(
            timestamp=update_timestamp,
            **tp.dict(),
        )
        try:
            session.merge(token_pool_price)
            session.commit()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    run_token_prices(session_factory())
