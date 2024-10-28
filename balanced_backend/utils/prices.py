from __future__ import annotations

import logging

import networkx as nx
from pydantic import BaseModel, ConfigDict
from starlette.config import Config

from balanced_backend.utils.rpc import get_band_price
from balanced_backend.log import logger

class PoolPrice(BaseModel):
    """
    Minimal representation of a pool to calculate the price. We do this so we can
     decouple the pricing algorithm from the backend representation in case we want to
     call this in multiple different places such as in the series, token, or as some
     immediate call.
    """
    pool_id: int
    total_supply: float
    quote_address: str
    base_address: str
    price: float

    model_config = ConfigDict(
        extra="ignore",
    )


class TokenPrice(BaseModel):
    """Minimal representation of a token to calculate the price."""
    address: str
    price: float | None = None
    path: list | None = None

    model_config = ConfigDict(
        extra="ignore",
    )


def get_token_prices(
        pools: list[PoolPrice],
        tokens: list[TokenPrice],
        *,
        icx_price: float = None,
        root_address: str = 'ICX',
) -> list[TokenPrice]:
    if icx_price is None:
        # Need to seed our search with ICX price
        icx_price = get_band_price(symbol='ICX')

    G = nx.Graph()

    # Initialize all the edges
    for p in pools:
        if p.total_supply != 0:
            weight = 1 / p.total_supply
        else:
            weight = 1
        G.add_edge(p.quote_address, p.base_address, weight=weight, data=p)

    for t in tokens:
        if t.address == root_address:
            t.price = icx_price
        else:
            # Zero out the prices for all the pools as these will later be updated
            t.price = None
        # Set metadata about node / token
        G.add_node(t.address, data=t)

    # Now we are going to iterate through all to tokens / nodes, find the path to the
    # node, and calculate the price based on the prior nodes. This uses the price of a
    # node if it has already been calculated.
    for t in tokens:
        # Get the shortest weighted path to the target token
        try:
            path = nx.dijkstra_path(G, source=root_address, target=t.address)
        except nx.exception.NetworkXNoPath:
            # Sometimes no swaps (ie just deployed)
            # https://github.com/balancednetwork/balanced-backend/issues/62
            logger.info(f"Missing data for {t.address}")
            continue

        # Store the path in the DB
        t.path = path

        for p in range(0, len(path) - 1):
            pool = G.get_edge_data(path[p], path[p + 1])['data']

            token_0 = G.nodes[path[p]]['data']
            token_1 = G.nodes[path[p + 1]]['data']

            if token_1.price is not None:
                # We already know the price
                continue

            if pool.base_address == token_0.address:
                try:
                    token_1.price = token_0.price / pool.price
                except ZeroDivisionError:
                    logger.info(f"error - zero division \npool={pool}\ntoken_0={token_0}\ntoken_1={token_1}")
            else:
                try:
                    token_1.price = pool.price * token_0.price
                except TypeError as e:
                    logger.info(f"Encountered error={e} \npool={pool}\ntoken_0={token_0}\ntoken_1={token_1}")
    return tokens
