from sqlmodel import select
from typing import TypedDict, List
from loguru import logger

from balanced_backend.tables.tokens import Token


class StableToken(TypedDict):
    address: str
    stable: bool
    stability: bool


stable_tokens: List[StableToken] = [
    {
        "address": "cx22319ac7f412f53eabe3c9827acf5e27e9c6a95f",
        "stable": True,
        "stability": True,
    },
    {
        "address": "cxf0a30d09ade391d7b570908b9b46cfa5b3cbc8f8",
        "stable": True,
        "stability": True,
    },
]


def mark_tokens_as_stable(session):
    for t in stable_tokens:
        result = session.execute(select(Token).where(Token.address == t["address"]))
        token = result.scalars().first()
        if token is not None:
            token.is_stable = t["stable"]
            token.in_stability = t["stability"]
            session.merge(token)
        else:
            logger.info("Token not in DB")

    session.commit()
