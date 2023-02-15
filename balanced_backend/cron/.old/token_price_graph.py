from typing import TYPE_CHECKING
from sqlmodel import select
from pydantic import BaseModel
from loguru import logger
import networkx as nx

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


def build_pool_graph(pools: list[Pool], root_pools: list[str]) -> nx.Graph:
    G = nx.Graph()

    root_pools = [
        pools.pop(i) for i, v in enumerate(pools) if v.quote_symbol in root_pools
    ]

    for p in root_pools:
        G.add_node(p.quote_symbol, data=p)

    for p in pools:
        edge = (p.base_name, p.quote_name)
        G.add_edge(*edge, data=p)
    return G


def run_token_prices(session: 'Session'):
    logger.info("Running token prices cron...")

    result = session.execute(select(Pool).where(Pool.chain_id == settings.CHAIN_ID))
    pools: list[Pool] = result.scalars().all()
    update_timestamp = pools[0].last_updated_timestamp

    # Output is stored here then we take weighted average at the end
    token_prices: list[TokenPrice] = []

    # Need to seed our
    icx_price = get_band_price(symbol='ICX')

    # Build graph of pools
    G = build_pool_graph(pools, root_pools=['ICX'])

    for n, nbrsdict in G.adjacency():
        print(n)

        for nbr, keydict in nbrsdict.items():
            print(nbr)

            for key, eattr in keydict.items():
                print()
                if "weight" in eattr:
                    # Do something useful with the edges
                    pass


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    run_token_prices(session_factory())
