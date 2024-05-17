from typing import TYPE_CHECKING, Callable
from loguru import logger
from datetime import datetime

from balanced_backend.crud.pools import get_pools
from balanced_backend.crud.dex import get_dex_swaps
from balanced_backend.cache.cache import cache
from balanced_backend.models.coingecko import (
    PairsCoinGecko,
    TickerCoinGecko,
    OrderBookCoinGecko,
    HistoricalCoinGecko,
)
from balanced_backend.tables.pools import Pool
from balanced_backend.utils.pools import get_cached_pool_stats
from balanced_backend.config import settings

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def clean_pools_for_coingecko(pools: list[Pool]) -> list[Pool]:
    """
    Coingecko calculates their prices with a blackbox thingamajig that is wrong due to
     issues (we think) in how the use low liquidity / depleted pools in price resolution
     and / or they think sicx is icx. Regardless, they are a nightmare to deal with
     managing to send one message every 6 months without reading the prior response.
     Anyways, we are filtering out low liquidity pools and making icx the same as sicx.
    """
    output = []
    for p in pools:
        if p.base_liquidity + p.quote_liquidity < settings.COINGECKO_LIQUIDITY_CUTOFF:
            # Skip low pools
            continue
        if p.name == 'sICX_ICX':
            p.price = 1
            p.price_24h = 1
            p.price_24h_high = 1
            p.price_24h_low = 1

        output.append(p)
    return output


def update_coingecko_pairs(session: 'Session'):
    logger.info("Updating coingecko pairs cache...")
    pools = clean_pools_for_coingecko(get_pools(session=session))

    summaries = []
    for p in pools:
        names = p.name.split('/')
        summaries.append(PairsCoinGecko(
            ticker_id='_'.join(names),
            base=names[0],
            target=names[1],
            pool_id='_'.join([p.base_address, p.quote_address]),
        ).dict())
    cache.coingecko_pairs = summaries


def update_coingecko_tickers(session: 'Session'):
    logger.info("Updating coingecko tickers cache...")
    pools = clean_pools_for_coingecko(get_pools(session=session))

    tickers = []
    for p in pools:
        names = p.name.split('/')
        tickers.append(TickerCoinGecko(
            ticker_id='_'.join(names),
            base_currency=names[0],
            target_currency=names[1],
            last_price=p.price,
            base_volume=p.base_volume_24h,
            target_volume=p.quote_volume_24h,
            pool_id='_'.join([p.base_address, p.quote_address]),
            liquidity_in_usd=p.base_liquidity + p.quote_liquidity,
            bid=p.price * .997,
            ask=p.price * 1.003,
            high=p.price_24h_high,
            low=p.price_24h_low,
        ).dict())
    cache.coingecko_tickers = tickers


def update_coingecko_orderbook(session: 'Session'):
    logger.info("Updating coingecko orderbook cache...")
    pools = clean_pools_for_coingecko(get_pools(session=session))

    order_book_dict = {}
    for p in pools:
        names = p.name.split('/')
        market_pair = '_'.join(names)

        order_book_dict[market_pair] = OrderBookCoinGecko(
            # Note they ask for milliseconds
            timestamp=int(datetime.now().timestamp() * 1e3),
            ticker_id='_'.join(names),
            bids=[
                [p.price * .997, 1]
            ],
            asks=[
                [p.price * 1.003, 1]
            ],
        ).dict()
    cache.coingecko_orderbook = order_book_dict


def update_coingecko_historical(session: 'Session'):
    logger.info("Updating coingecko historical cache...")
    pools = clean_pools_for_coingecko(get_pools(session=session))

    trades = {}
    for p in pools:
        names = p.name.split('/')
        market_pair = '_'.join(names)
        trades[market_pair] = {
            'buy': [],
            'sell': [],
        }

        swaps = get_dex_swaps(
            session=session,
            pool_id=p.pool_id,
            limit=100,
        )

        for s in swaps:
            pool_data = get_cached_pool_stats(p.pool_id)
            if s.from_token == pool_data['quote_address']:
                swap_type = "sell"
            else:
                swap_type = "buy"

            trades[market_pair][swap_type].append(HistoricalCoinGecko(
                trade_id=s.transaction_hash,
                price=s.effective_fill_price_decimal,
                base_volume=s.base_token_value_decimal,
                target_volume=s.quote_token_value_decimal,
                # Note they ask for milliseconds
                trade_timestamp=int(s.timestamp * 1e3),
                type=swap_type,
            ).dict())
    cache.coingecko_historical = trades
