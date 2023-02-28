from typing import TYPE_CHECKING
from sqlmodel import select

from balanced_backend.config import settings
from balanced_backend.tables.tokens import Token

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_tokens(session: 'Session') -> list[Token]:
    result = session.execute(select(Token).where(Token.chain_id == settings.CHAIN_ID))
    return result.scalars().all()
