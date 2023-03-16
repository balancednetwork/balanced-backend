from typing import TYPE_CHECKING
from fastapi import APIRouter

from balanced_backend.db import session_factory
from balanced_backend.cache.cache import cache
from balanced_backend.cache import coingecko

if TYPE_CHECKING:
    from balanced_backend.models.coingecko import (
        PairsCoinGecko,
        TickerCoinGecko,
        OrderBookCoinGecko,
        HistoricalCoinGecko,
    )

router = APIRouter()


@router.get("/pairs")
async def get_coingecko_summary() -> list['PairsCoinGecko']:
    output = cache.coingecko_pairs
    if len(output) == 0:
        with session_factory() as session:
            coingecko.update_coingecko_pairs(session=session)
        output = cache.coingecko_pairs
    return output


@router.get("/tickers")
async def get_coingecko_ticker() -> dict[str, 'TickerCoinGecko']:
    output = cache.coingecko_tickers
    if len(output) == 0:
        with session_factory() as session:
            coingecko.update_coingecko_tickers(session=session)
        output = cache.coingecko_tickers
    return output


@router.get("/orderbook")
async def get_coingecko_orderbook(
        ticker_id: str = None,
) -> dict[str, 'OrderBookCoinGecko']:
    if ticker_id is None:
        return cache.coingecko_orderbook

    try:
        output = cache.coingecko_orderbook[ticker_id]
    except KeyError:
        with session_factory() as session:
            coingecko.update_coingecko_orderbook(session=session)
        output = cache.coingecko_orderbook[ticker_id]
    return output


@router.get("/historical")
async def get_coingecko_trades(
        ticker_id: str = None,
) -> dict[str, 'HistoricalCoinGecko']:
    if ticker_id is None:
        return cache.coingecko_historical

    try:
        output = cache.coingecko_historical[ticker_id]
    except KeyError:
        with session_factory() as session:
            coingecko.update_coingecko_historical(session=session)
        output = cache.coingecko_historical[ticker_id]
    return output
