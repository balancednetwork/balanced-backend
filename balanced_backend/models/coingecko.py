from pydantic import BaseModel, Field


class PairsCoinGecko(BaseModel):
    ticker_id: str
    base: str
    target: str
    pool_id: str


class TickerCoinGecko(BaseModel):
    """
    Indented based on market pair - ex. BTC_USDT.
    Ex:
    {
       "BTC_USDT":{
          "base_id":"1",
          "quote_id":"825",
          "last_price":"10000",
          "quote_volume":"20000",
          "base_volume":"2",
          "isFrozen":"0"
       },
    ...
    }
    """
    # Enable this when getting a unified asset ID
    # https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?CoinGecko_PRO_API_KEY=UNIFIED-CRYPTOASSET-INDEX&listing_status=active
    ticker_id: str
    base_currency: str
    target_currency: str
    last_price: float
    base_volume: float
    target_volume: float
    pool_id: str
    liquidity_in_usd: float
    bid: float
    ask: float
    high: float
    low: float


class OrderBookCoinGecko(BaseModel):
    timestamp: int
    ticker_id: str
    bids: list
    asks: list


class HistoricalCoinGecko(BaseModel):
    trade_id: str
    price: float
    base_volume: float
    target_volume: float
    trade_timestamp: int
    type: str

# class Contract(BaseModel):
#     ticker_id: str
#     base_currency: str
#     quote_currency: str
#     last_price: float
#     base_volume: float
#     # USD_volume: float
#     quote_volume: float
#     bid: float
#     ask: float
#     high: float
#     low: float
#     product_type: str
#     open_interest: float
#     open_interest_usd: float
#     index_price: float
#     creation_timestamp: int
#     expiry_timestamp: int
#     funding_rate: float
