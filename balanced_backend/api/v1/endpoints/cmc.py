from typing import TYPE_CHECKING
from fastapi import APIRouter

from balanced_backend.db import session_factory
from balanced_backend.cache.cache import cache
from balanced_backend.cache import cmc

if TYPE_CHECKING:
    from balanced_backend.models.cmc import (
        SummaryCMC,
        TickerCMC,
        OrderBookCMC,
        TradeCMC,
    )

router = APIRouter()


@router.get("/summary")
async def get_cmc_summary() -> list['SummaryCMC']:
    output = cache.cmc_summary
    if len(output) == 0:
        with session_factory() as session:
            cmc.update_cmc_summary(session=session)
        output = cache.cmc_summary
    return output


@router.get("/ticker")
async def get_cmc_ticker() -> dict[str, 'TickerCMC']:
    output = cache.cmc_ticker
    if len(output) == 0:
        with session_factory() as session:
            cmc.update_cmc_tickers(session=session)
        output = cache.cmc_ticker
    return output


@router.get("/orderbook/{market_pair}")
async def get_cmc_orderbook(
        market_pair: str,
) -> dict[str, 'OrderBookCMC']:
    try:
        output = cache.cmc_order_book[market_pair]
    except KeyError:
        with session_factory() as session:
            cmc.update_cmc_order_book(session=session)
        output = cache.cmc_order_book[market_pair]
    return output


@router.get("/trades/{market_pair}")
async def get_cmc_trades(
        market_pair: str,
) -> dict[str, 'TradeCMC']:
    try:
        output = cache.cmc_trades[market_pair]
    except KeyError:
        with session_factory() as session:
            cmc.update_cmc_trades(session=session)
        output = cache.cmc_trades[market_pair]
    return output
