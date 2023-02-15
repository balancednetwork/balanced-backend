from typing import TYPE_CHECKING
from sqlmodel import select
from loguru import logger

from balanced_backend.config import settings
from balanced_backend.tables.tokens import Token, TokenPool

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
        total_supply = sum([i.supply for i in token_pool_list])

        weighted_price = supply_weighted_price / total_supply

        token.price = weighted_price
        token.total_supply = total_supply

        try:
            session.merge(token)
            session.commit()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    run_token_prices(session_factory())
