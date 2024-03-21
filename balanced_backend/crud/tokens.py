from typing import TYPE_CHECKING
from sqlmodel import select

from balanced_backend.config import settings
from balanced_backend.tables.tokens import Token

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_tokens(session: 'Session') -> list[Token]:
    result = session.execute(select(Token).where(Token.chain_id == settings.CHAIN_ID))
    return result.scalars().all()


def get_token_price(session: 'Session', address: str, timestamp: int = None) -> float:
    query = select(Token.price).where(
        Token.chain_id == settings.CHAIN_ID).where(
        Token.address == address,
    )
    if timestamp is not None:
        query = query.where(Token.timestamp == timestamp)
    result = session.execute(query)
    return result.scalars().first()
