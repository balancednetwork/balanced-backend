from pydantic import BaseModel, Field


class SummaryCMC(BaseModel):
    trading_pairs: str
    base_currency: str
    quote_currency: str
    last_price: float
    lowest_ask: float
    highest_bid: float
    base_volume: float
    quote_volume: float
    price_change_percent_24h: float
    highest_price_24h: float
    lowest_price_24h: float


class TickerCMC(BaseModel):
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
    # https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?CMC_PRO_API_KEY=UNIFIED-CRYPTOASSET-INDEX&listing_status=active
    # base_id: float
    # quote_id: float
    last_price: float
    base_volume: float
    quote_volume: float
    isFrozen: int = Field(0)


class OrderBookCMC(BaseModel):
    timestamp: int
    bids: list
    asks: list


class TradeCMC(BaseModel):
    trade_id: str
    price: float
    base_volume: float
    quote_volume: float
    timestamp: int
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
