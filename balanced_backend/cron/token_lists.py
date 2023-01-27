from typing import TYPE_CHECKING
import requests
from sqlmodel import select

from balanced_backend.tables.tokens import Token
from balanced_backend.config import settings

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_icon_dict():
    """Duplicating ICON_DICT for each network."""
    icon_token_dict = {
        'address': 'ICON',
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


def add_tokens_to_db(
        session: 'Session',
        tokens_json: dict,
        token_addresses: list,
        token_type: str
):
    for t in tokens_json['tokens']:
        if t['address'] not in token_addresses and t['chainId'] == settings.CHAIN_ID:
            token_db = Token(
                address=t['address'],
                chain_id=t['chainId'],
                name=t['name'],
                symbol=t['symbol'],
                decimals=t['decimals'],
                logo_uri=t['logoURI'],
                type=token_type,
            )

            session.merge(token_db)
            session.commit()


def build_token_list(
        session: 'Session',
):
    community_tokens_uri = "https://raw.githubusercontent.com/balancednetwork/balanced-network-interface/master/src/store/lists/communitylist.json"
    token_list_uri = "https://raw.githubusercontent.com/balancednetwork/balanced-network-interface/master/src/store/lists/tokenlist.json"

    result = session.execute(select(Token))
    tokens = result.scalars().all()

    token_addresses = [i.address for i in tokens]

    # ICX is a special case and needs to be manually added
    add_tokens_to_db(
        session=session,
        tokens_json=get_icon_dict(),
        token_addresses=token_addresses,
        token_type="community",
    )
    # Balanced tokens
    add_tokens_to_db(
        session=session,
        tokens_json=get_token_json(tokens_uri=community_tokens_uri),
        token_addresses=token_addresses,
        token_type="community",
    )
    # Community tokens
    add_tokens_to_db(
        session=session,
        tokens_json=get_token_json(tokens_uri=token_list_uri),
        token_addresses=token_addresses,
        token_type="balanced",
    )


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    build_token_list(session_factory())
