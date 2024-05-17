from typing import TYPE_CHECKING
from fastapi import APIRouter, HTTPException

from balanced_backend.api.v1.endpoints._utils import sleep_while_empty_cache
from balanced_backend.cache.cache import cache

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
    await sleep_while_empty_cache('cmc_summary')
    return cache.cmc_summary


@router.get("/ticker")
async def get_cmc_ticker() -> dict[str, 'TickerCMC']:
    await sleep_while_empty_cache('cmc_tickers')
    return cache.cmc_tickers


@router.get("/orderbook/{market_pair}")
async def get_cmc_orderbook(
        market_pair: str,
) -> dict[str, 'OrderBookCMC']:
    await sleep_while_empty_cache('cmc_orderbook')
    try:
        return cache.cmc_orderbook[market_pair]
    except KeyError:
        raise HTTPException(
            status_code=204,
            detail=f"market_pair not found - check /summary for available pairs."
        )


@router.get("/trades/{market_pair}")
async def get_cmc_trades(
        market_pair: str,
) -> dict[str, 'TradeCMC']:
    await sleep_while_empty_cache('cmc_trades')
    try:
        return cache.cmc_trades[market_pair]
    except KeyError:
        raise HTTPException(
            status_code=204,
            detail=f"market_pair not found - check /summary for available pairs."
        )
