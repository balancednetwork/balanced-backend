from loguru import logger
from prometheus_client import start_http_server
from typing import Callable, TypedDict
from apscheduler.schedulers.background import BlockingScheduler
from typing import TYPE_CHECKING

from balanced_backend.config import settings
from balanced_backend.db import session_factory

from balanced_backend.cron import (
    methods,
    volumes,
    token_lists,
    pool_lists,
    pool_prices,
    token_pools,
    token_prices,
    pool_series,
)
from balanced_backend.cron.contracts import dex_swaps

if TYPE_CHECKING:
    from typing import Callable


class Cron(TypedDict):
    func: Callable
    interval: int


CRONS: list[Cron] = [
    {
        'func': volumes.run_volumes,
        'interval': 600,
    },
    {
        'func': methods.run_methods,
        'interval': 600,
    },
    {
        'func': token_lists.run_token_list,
        'interval': 86400 / 4,
    },
    {
        'func': pool_lists.run_pool_list,
        'interval': 60 * 60,
    },
    {
        'func': pool_prices.run_pool_prices,
        'interval': 600,
    },
    {
        'func': token_pools.run_token_pool_prices,
        'interval': 600,
    },
    {
        'func': token_prices.run_token_prices,
        'interval': 600,
    },
    {
        'func': dex_swaps.run_dex_swaps,
        'interval': 60,
    },
    {
        'func': pool_series.run_pool_volumes_series,
        'interval': 600,
    },
]


def main():
    logger.info("Starting metrics server.")
    start_http_server(settings.METRICS_PORT, settings.METRICS_ADDRESS)

    sched = BlockingScheduler()

    with session_factory() as session:
        for i in CRONS:
            # Run the jobs immediately in order
            i['func'](session=session)

            # Then run them in the scheduler
            sched.add_job(
                func=i['func'],
                trigger="interval",
                args=[session],
                seconds=i['interval'],
                id=i['func'].__name__
            )

        sched.start()


if __name__ == '__main__':
    main()