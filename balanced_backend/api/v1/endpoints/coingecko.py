from __future__ import annotations

from typing import Union

from fastapi import APIRouter, HTTPException, Query
from starlette.responses import Response

from balanced_backend.api.v1.endpoints._utils import sleep_while_empty_cache
from balanced_backend.cache.cache import cache

from balanced_backend.models.coingecko import (
    PairsCoinGecko,
    TickerCoinGecko,
    OrderBookCoinGecko,
    HistoricalCoinGecko,
)

router = APIRouter()


# Per this guide
# https://docs.google.com/document/d/1v27QFoQq1SKT3Priq3aqPgB70Xd_PnDzbOCiuoCyixw/edit


@router.get("/pairs")
async def get_coingecko_summary() -> list[PairsCoinGecko]:
    await sleep_while_empty_cache("coingecko_pairs")
    return cache.coingecko_pairs


@router.get("/tickers")
async def get_coingecko_ticker() -> list[TickerCoinGecko]:
    await sleep_while_empty_cache("coingecko_tickers")
    return cache.coingecko_tickers


@router.get("/orderbook")
async def get_coingecko_orderbook(
    ticker_id: str = None,
) -> dict[str, OrderBookCoinGecko] | OrderBookCoinGecko:
    await sleep_while_empty_cache("coingecko_orderbook")
    if ticker_id is None:
        return cache.coingecko_orderbook
    try:
        return cache.coingecko_orderbook[ticker_id]
    except KeyError:
        raise HTTPException(
            status_code=204,
            detail=f"ticker_id not found - check /summary for available pairs.",
        )


@router.get("/historical_trades")
async def get_coingecko_trades(
    response: Response,
    ticker_id: str = Query(None),
    type: str = Query(None, regex="^(buy|sell)$"),
) -> Union[
    dict[str, dict[str, list[HistoricalCoinGecko]]],
    dict[str, list[HistoricalCoinGecko]],
    list[HistoricalCoinGecko],
]:
    await sleep_while_empty_cache("coingecko_historical")

    if ticker_id is None:
        response.headers["x-total-count"] = str(len(cache.coingecko_historical))
        output = cache.coingecko_historical
        if type:
            for k, v in output.items():
                output[k] = output[k][type]
        return output
    try:
        output = cache.coingecko_historical[ticker_id]
        if type:
            return output[type]
        return output

    except KeyError:
        raise HTTPException(
            status_code=422,
            detail=f"ticker_id not found - check /summary for available pairs.",
        )
