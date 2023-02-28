from typing import TYPE_CHECKING
from loguru import logger
from datetime import datetime

from balanced_backend.crud.pools import get_pools
from balanced_backend.crud.dex import get_dex_swaps
from balanced_backend.cache.cache import cache
from balanced_backend.models.cmc import SummaryCMC, TickerCMC, OrderBookCMC, TradeCMC
from balanced_backend.utils.pools import get_cached_pool_stats

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def update_cmc_summary(session: 'Session'):
    logger.info("Updating cmc summary cache...")
    pools = get_pools(session=session)

    summaries = []
    for p in pools:
        if p.price != 0:
            price_change_percent_24h = (p.price - p.price_24h) / p.price * 100
        else:
            price_change_percent_24h = 0.0

        names = p.name.split('/')
        summaries.append(SummaryCMC(
            trading_pairs='_'.join(names),
            base_currency=names[0],
            quote_currency=names[1],
            last_price=p.price,
            price_change_percent_24h=price_change_percent_24h,
            # Sourced from dex swaps
            base_volume=p.base_volume_24h,
            quote_volume=p.quote_volume_24h,
            highest_price_24h=p.price_24h_high,
            lowest_price_24h=p.price_24h_low,
            highest_bid=p.price_24h_high,  # highest_price_24h
            lowest_ask=p.price_24h_low,  # lowest_price_24h
        ))
    cache.cmc_summary = summaries


def update_cmc_tickers(session: 'Session'):
    logger.info("Updating cmc tickers cache...")
    pools = get_pools(session=session)

    tickers = {}
    for p in pools:
        names = p.name.split('/')
        market_pair = '_'.join(names)

        tickers[market_pair] = TickerCMC(
            last_price=p.price,
            base_volume=p.base_volume_24h,
            quote_volume=p.quote_volume_24h,
            isFrozen=0,
        )
    cache.cmc_ticker = tickers


def update_cmc_order_book(session: 'Session'):
    logger.info("Updating cmc order book cache...")
    pools = get_pools(session=session)

    order_book_dict = {}
    for p in pools:
        names = p.name.split('/')
        market_pair = '_'.join(names)

        order_book_dict[market_pair] = OrderBookCMC(
            timestamp=int(datetime.now().timestamp() * 1e6),
            bids=[],
            asks=[],
        )
    cache.cmc_order_book = order_book_dict


def update_cmc_trades(session: 'Session'):
    logger.info("Updating cmc cmc trades cache...")
    pools = get_pools(session=session)

    trades = {}
    for p in pools:
        names = p.name.split('/')
        market_pair = '_'.join(names)
        trades[market_pair] = []
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

            trades[market_pair].append(TradeCMC(
                trade_id=s.transaction_hash,
                price=s.effective_fill_price_decimal,
                base_volume=s.base_token_value_decimal,
                quote_volume=s.quote_token_value_decimal,
                timestamp=int(s.timestamp * 1e6),
                type=swap_type,
            ))
    cache.cmc_trades = trades
