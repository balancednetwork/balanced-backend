from pydantic import BaseModel

from balanced_backend.models.cmc import SummaryCMC, TickerCMC, OrderBookCMC, TradeCMC


class Cache(BaseModel):
    cmc_summary: list[SummaryCMC] = []
    cmc_ticker: dict[str, TickerCMC] = {}
    cmc_order_book: dict[str, OrderBookCMC] = {}
    cmc_trades: dict[str, list[TradeCMC]] = {}


cache = Cache()
