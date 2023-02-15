from typing import TYPE_CHECKING
import requests
from sqlmodel import select
from loguru import logger
from pydantic import BaseModel

from balanced_backend.tables.tokens import Token
from balanced_backend.config import settings
from balanced_backend.utils.rpc import get_pool_stats, get_contract_method_str
from balanced_backend.cron.pool_lists import get_pools

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class TokenListToken(BaseModel):
    """Validate the token list field."""
    address: str
    chainId: int
    name: str
    symbol: str
    decimals: int
    logoURI: str


def get_icon_dict():
    """Duplicating ICON_DICT for each network."""
    icon_token_dict = {
        'address': 'ICX',
        'name': 'ICON',
        'symbol': 'ICX',
        'decimals': 18,
        'logoURI': 'https://s2.coinmarketcap.com/static/img/coins/200x200/2099.png',
    }
    output = {'tokens': []}
    for i in [1, 2, 7]:  # chain ids
        icon_token_dict['chainId'] = i
        output['tokens'].append(icon_token_dict.copy())
    return output


def get_token_json(tokens_uri: str) -> dict:
    r = requests.get(tokens_uri)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception("Couldn't fetch token uri...")


def get_token_from_db(session: 'Session', address: str) -> Token:
    result = session.execute(select(Token).where(
        Token.address == address
    ).where(
        Token.chain_id == settings.CHAIN_ID
    ))
    token = result.scalars().first()  # Where condition on PKs -> one record always
    return token


def create_token(session: 'Session', address: str, decimals: str):
    token_db = Token(
        address=address,
        symbol=get_contract_method_str(
            to_address=address, method='symbol'
        ),
        name=get_contract_method_str(
            to_address=address, method='name'
        ),
        decimals=int(decimals, 16),
        chain_id=settings.CHAIN_ID,
        type='community',
    )
    session.merge(token_db)
    session.commit()


def add_tokens_to_db(
        session: 'Session',
        tokens_json: dict,
        # tokens: list[Token],
        token_type: str
):
    for t in tokens_json['tokens']:
        # Validate the token list input
        token_item = TokenListToken(**t)

        if token_item.chainId != settings.CHAIN_ID:
            # Skip tokens from other chains
            continue

        # Get the token from the DB
        token = get_token_from_db(session=session, address=token_item.address)

        if token is None:
            token = Token(
                address=token_item.address,
                chain_id=token_item.chainId,
                name=token_item.name,
                symbol=token_item.symbol,
                decimals=token_item.decimals,
                logo_uri=token_item.logoURI,
                type=token_type,
            )
        else:
            # Some fields are interpreted like when we
            if token_item.name != "":
                token.name = token_item.name
            if token_item.logoURI != "":
                token.logo_uri = token_item.logoURI

            token.symbol = token_item.symbol
            token.decimals = token_item.decimals
            token.type = token_type

        session.merge(token)
        session.commit()


def run_token_list(
        session: 'Session',
):
    logger.info("Running token lists cron...")

    community_tokens_uri = "https://raw.githubusercontent.com/balancednetwork/balanced-network-interface/master/src/store/lists/communitylist.json"
    token_list_uri = "https://raw.githubusercontent.com/balancednetwork/balanced-network-interface/master/src/store/lists/tokenlist.json"

    # ICX is a special case and needs to be manually added
    add_tokens_to_db(
        session=session,
        tokens_json=get_icon_dict(),
        token_type="balanced",
    )
    # Balanced tokens
    add_tokens_to_db(
        session=session,
        tokens_json=get_token_json(tokens_uri=token_list_uri),
        token_type="balanced",
    )
    # Community tokens
    add_tokens_to_db(
        session=session,
        tokens_json=get_token_json(tokens_uri=community_tokens_uri),
        token_type="community",
    )

    # Finally grab all the tokens that are missing via the getPoolStats
    pools = get_pools()
    for p in pools:
        token = get_token_from_db(session=session, address=p['base_token'])
        if token is None:
            create_token(
                session=session,
                address=p['base_token'],
                decimals=p['base_decimals']
            )

        token = get_token_from_db(session=session, address=p['quote_token'])
        if token is None:
            if p['quote_token'] is None:
                # ICX case -> p['quote_token'] is None
                continue

            create_token(
                session=session,
                address=p['quote_token'],
                decimals=p['quote_decimals']
            )


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    run_token_list(session_factory())
