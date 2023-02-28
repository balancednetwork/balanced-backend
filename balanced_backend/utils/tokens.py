from balanced_backend.db import session_factory
from balanced_backend.crud.tokens import get_tokens
from balanced_backend.tables.tokens import Token

TOKEN_ADDRESSES: dict[str, Token] = {}


def get_cached_token_info(address: str) -> Token:
    try:
        return TOKEN_ADDRESSES[address]
    except KeyError:
        with session_factory() as session:
            tokens = get_tokens(session=session)
            for i in tokens:
                TOKEN_ADDRESSES[i.address] = i
        return TOKEN_ADDRESSES[address]
