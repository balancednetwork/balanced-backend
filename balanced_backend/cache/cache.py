from pydantic import BaseModel

from balanced_backend.models import cmc
from balanced_backend.models import coingecko


class Cache(BaseModel):
    cmc_summary: list[cmc.SummaryCMC] = []
    cmc_tickers: dict[str, cmc.TickerCMC] = {}
    cmc_orderbook: dict[str, cmc.OrderBookCMC] = {}
    cmc_trades: dict[str, list[cmc.TradeCMC]] = {}

    coingecko_pairs: list[coingecko.PairsCoinGecko] = []
    coingecko_tickers: list[coingecko.TickerCoinGecko] = []
    coingecko_orderbook: dict[str, list[coingecko.OrderBookCoinGecko]] = {}
    coingecko_historical: dict[str, list[coingecko.HistoricalCoinGecko]] = {}


cache = Cache()
