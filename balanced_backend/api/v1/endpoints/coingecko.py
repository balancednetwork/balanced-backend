from typing import TYPE_CHECKING
from fastapi import APIRouter, HTTPException
from starlette.responses import Response

from balanced_backend.api.v1.endpoints._utils import sleep_while_empty_cache
from balanced_backend.cache.cache import cache

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
    await sleep_while_empty_cache('coingecko_pairs')
    return cache.coingecko_pairs


@router.get("/tickers")
async def get_coingecko_ticker() -> dict[str, 'TickerCoinGecko']:
    await sleep_while_empty_cache('coingecko_tickers')
    return cache.coingecko_tickers


@router.get("/orderbook")
async def get_coingecko_orderbook(
        ticker_id: str = None,
) -> dict[str, 'OrderBookCoinGecko']:
    await sleep_while_empty_cache('coingecko_orderbook')
    if ticker_id is None:
        return cache.coingecko_orderbook
    try:
        return cache.coingecko_orderbook[ticker_id]
    except KeyError:
        raise HTTPException(
            status_code=204,
            detail=f"ticker_id not found - check /summary for available pairs."
        )



@router.get("/historical_trades")
async def get_coingecko_trades(
        response: Response,
        ticker_id: str = None,
) -> dict[str, 'HistoricalCoinGecko']:
    await sleep_while_empty_cache('coingecko_historical')
    if ticker_id is None:
        response.headers["x-total-count"] = str(len(cache.coingecko_historical))
        return cache.coingecko_historical
    try:
        return cache.coingecko_historical[ticker_id]
    except KeyError:
        raise HTTPException(
            status_code=204,
            detail=f"ticker_id not found - check /summary for available pairs."
        )
