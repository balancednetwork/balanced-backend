import asyncio

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
        'interval': 60,
    },
    {
        'func': cmc.update_cmc_order_book,
        'interval': 60,
    },
    {
        'func': cmc.update_cmc_tickers,
        'interval': 60,
    },
    {
        'func': cmc.update_cmc_trades,
        'interval': 60 * 10,
    },
    {
        'func': coingecko.update_coingecko_pairs,
        'interval': 60,
    },
    {
        'func': coingecko.update_coingecko_orderbook,
        'interval': 60,
    },
    {
        'func': coingecko.update_coingecko_tickers,
        'interval': 60,
    },
    {
        'func': coingecko.update_coingecko_historical,
        'interval': 60 * 10,
    },
]


def run_cron_with_session(cron: Callable):
    with session_factory() as session:
        logger.info(f"Running {cron.__name__}...")
        cron(session=session)
        logger.info(f"Finished {cron.__name__}...")


async def run_all_crons():
    tasks = [run_cron_with_session(i['func']) for i in CRONS]
    await asyncio.gather(*tasks)


def cache_cron():
    logger.info("Starting metrics server.")
    sched = BlockingScheduler()

    # # Run the jobs immediately in parallel
    # asyncio.run(run_all_crons())

    for i in CRONS:
        # Run right away
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
