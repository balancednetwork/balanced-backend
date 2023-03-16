from loguru import logger
from typing import TypedDict, Callable
from apscheduler.schedulers.background import BlockingScheduler

from balanced_backend.cache import cmc, coingecko
from balanced_backend.db import session_factory


class Cron(TypedDict):
    func: Callable
    interval: int


CRONS: list[Cron] = [
    {
        'func': cmc.update_cmc_summary,
        'interval': 60 * 60,
    },
    {
        'func': cmc.update_cmc_order_book,
        'interval': 60 * 60,
    },
    {
        'func': cmc.update_cmc_tickers,
        'interval': 60 * 60,
    },
    {
        'func': cmc.update_cmc_trades,
        'interval': 60 * 60,
    },
    {
        'func': coingecko.update_coingecko_pairs,
        'interval': 60 * 60,
    },
    {
        'func': coingecko.update_coingecko_orderbook,
        'interval': 60 * 60,
    },
    {
        'func': coingecko.update_coingecko_tickers,
        'interval': 60 * 60,
    },
    {
        'func': coingecko.update_coingecko_historical,
        'interval': 60 * 60,
    },
]


def run_cron_with_session(cron: Callable):
    with session_factory() as session:
        cron(session=session)


def cache_cron():
    logger.info("Starting metrics server.")
    sched = BlockingScheduler()

    for i in CRONS:
        # Run the jobs immediately in order
        run_cron_with_session(i['func'])

        # Then run them in the scheduler
        sched.add_job(
            func=run_cron_with_session,
            trigger="interval",
            args=[i['func']],
            seconds=i['interval'],
            id=i['func'].__name__
        )

    sched.start()
