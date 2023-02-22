from typing import TYPE_CHECKING
from sqlmodel import select
from loguru import logger

from balanced_backend.config import settings
from balanced_backend.tables.tokens import Token, TokenPool
from balanced_backend.utils.api import get_token_holders
from balanced_backend.utils.supply import get_total_supply

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def run_token_prices(session: 'Session'):
    logger.info("Running token prices cron...")

    result = session.execute(select(Token).where(Token.chain_id == settings.CHAIN_ID))
    token_list: list[Token] = result.scalars().all()

    for token in token_list:
        result = session.execute(select(TokenPool).where(
            TokenPool.chain_id == settings.CHAIN_ID
        ).where(
            TokenPool.address == token.address
        ))
        token_pool_list: list[TokenPool] = result.scalars().all()

        supply_weighted_price = sum([i.price * i.supply for i in token_pool_list])
        # Not the total supply as this is what is only in the pools
        pool_supply = sum([i.supply for i in token_pool_list])

        weighted_price = supply_weighted_price / pool_supply

        if token.address == 'ICX':
            token.holders = 0
        else:
            token.holders = get_token_holders(token.address)

        token.price = weighted_price
        token.total_supply = get_total_supply(
            address=token.address,
            decimals=token.decimals
        )

        session.merge(token)
        session.commit()

    logger.info("Ending token prices cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_token_prices(session=session)
