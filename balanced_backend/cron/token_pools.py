from typing import TYPE_CHECKING
from sqlmodel import select
from pydantic import BaseModel
from loguru import logger

from balanced_backend.config import settings
from balanced_backend.tables.tokens import TokenPool, TokenPrice
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
    supply: float
    pool_price: float
    pool_name: str
    reference_name: str
    reference_symbol: str
    reference_price: float
    reference_supply: float
    reference_address: str


def pop_pools_with_token(token_address: str, pools: list[Pool]) -> list[Pool]:
    """Pop a pool out given a token address in either to base or quote."""
    token_pools: list[Pool] = [
        pools.pop(i) for i, v in enumerate(pools)
        if v.quote_address == token_address or v.base_address ==  token_address
    ]
    return token_pools


def get_prices(
        token_prices: list[TokenPrice],
        pools: list[Pool],
        input_address: str,
        input_price: float,
) -> list[TokenPrice]:
    """
    Recursively look through the pools looking for token pairs with a known price. When
     a price is found, find all the pools that that token is paired with and calculate
     the price of the adjacent token based on that known price.
    """
    if len(pools) == 0:
        return token_prices

    target_pools = pop_pools_with_token(
        token_address=input_address,
        pools=pools,
    )

    added_tokens: list[dict] = []

    for p in target_pools:
        if p.base_address == input_address:
            name = p.quote_name
            symbol = p.quote_symbol
            price = input_price / p.price
            address = p.quote_address
            reference_name = p.base_name
            reference_symbol = p.base_symbol
            reference_address = p.base_address
            reference_supply = p.base_supply
            supply = p.quote_supply

        else:
            name = p.base_name
            symbol = p.base_symbol
            try:
                price = input_price * p.price
            except TypeError:
                logger.info(
                    f"ERORR: !! -> input_price: {input_price} p.price {p.price}"
                    f" address: {p.quote_address}")
            address = p.base_address
            reference_name = p.quote_name
            reference_symbol = p.quote_symbol
            reference_address = p.quote_address
            reference_supply = p.quote_supply
            supply = p.base_supply

        added_tokens.append({'address': address, 'price': price, 'pool_id': p.pool_id})

        # Store output
        token_prices.append(TokenPrice(
            name=name,
            address=address,
            symbol=symbol,
            price=price,
            supply=supply,
            pool_price=p.price,
            pool_id=p.pool_id,
            pool_name=p.name,
            reference_name=reference_name,
            reference_symbol=reference_symbol,
            reference_price=input_price,
            reference_address=reference_address,
            reference_supply=reference_supply,
        ))

    # Recurse to find
    for at in added_tokens:
        if at['price'] == 0:
            logger.info(f"Skipping token {at}")
            continue

        get_prices(
            token_prices=token_prices,
            pools=pools,
            input_address=at['address'],
            input_price=at['price'],
        )

    return token_prices


def run_token_pool_prices(session: 'Session'):
    logger.info("Running token pool prices cron...")

    result = session.execute(select(Pool).where(Pool.chain_id == settings.CHAIN_ID))
    pools: list[Pool] = result.scalars().all()

    update_timestamp = pools[0].last_updated_timestamp

    # Output is stored here then we take weighted average at the end
    token_prices: list[TokenPrice] = []

    # Need to seed our
    icx_price = get_band_price(symbol='ICX')
    logger.info(f"icx price: {icx_price}")

    token_prices = get_prices(
        token_prices=token_prices,
        pools=pools,
        input_address='ICX',
        input_price=icx_price,
    )

    for tp in token_prices:
        token_pool_price = TokenPool(
            timestamp=update_timestamp,
            chain_id=settings.CHAIN_ID,
            **tp.dict(),
        )
        reference_token_pool_price = TokenPool(
            timestamp=update_timestamp,
            pool_id=tp.pool_id,
            address=tp.reference_address,
            symbol=tp.reference_symbol,
            name=tp.reference_name,
            price=tp.reference_price,
            supply=tp.reference_supply,
            pool_price=tp.pool_price,
            pool_name=tp.pool_name,
            reference_address=tp.address,
            reference_name=tp.name,
            reference_price=tp.price,
            reference_supply=tp.supply,
            chain_id=settings.CHAIN_ID,
        )

        session.merge(token_pool_price)
        session.merge(reference_token_pool_price)
        session.commit()


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    run_token_pool_prices(session_factory())
