from time import sleep
from loguru import logger
from prometheus_client import start_http_server

from balanced_backend.config import settings
from balanced_backend.db import session_factory
from balanced_backend.metrics import prom_metrics

from balanced_backend.cron.methods import build_methods
from balanced_backend.cron.volumes import build_volumes
from balanced_backend.cron.token_lists import build_token_list
from balanced_backend.cron.pool_lists import build_pool_list

from multiprocessing.pool import ThreadPool

from apscheduler.schedulers.background import BlockingScheduler


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable
    from prometheus_client import Counter
    from sqlalchemy.orm import Session


def run_cron(
        session: Session,
        cron_function: Callable,
        sleep_period: int,
        metric: Counter = None,
        cron_name: str = None,
):
    while True:
        if cron_name is not None:
            logger.info(f"Starting {cron_name} cron")

        cron_function(session)

        if metric is not None:
            metric.inc()
        if cron_name is not None:
            logger.info(f"Sleeping {cron_name} cron")

        sleep(sleep_period)


def main():
    logger.info("Starting metrics server.")
    start_http_server(settings.METRICS_PORT, settings.METRICS_ADDRESS)

    sched = BlockingScheduler()

    with session_factory() as session:
        build_token_list(session=session)
        build_pool_list(session=session)

        sched.add_job(
            func=build_volumes,
            trigger="interval",
            args=[session],
            seconds=600,
            id='build-volumes'
        )

        sched.add_job(
            func=build_methods,
            trigger="interval",
            args=[session],
            seconds=600,
            id='build-methods'
        )

        sched.add_job(
            func=build_token_list,
            trigger="interval",
            args=[session],
            seconds=86400/4,
            id='build-tokens'
        )

        sched.add_job(
            func=build_pool_list,
            trigger="interval",
            args=[session],
            seconds=86400/4,
            id='build-tokens'
        )

        sched.start()

    # logger.info(f"Worker is a {worker_type}.")
    #
    # with session_factory() as session:
    #     logger.info("Starting crons")
    #     pool = ThreadPool(1)
    #     pool.apply_async(run_cron(
    #         session=session,
    #         cron_function=build_volumes,
    #         sleep_period=600,
    #         metric=prom_metrics.crons_ran,
    #         cron_name="build volumes",
    #     )
# )



# def main(worker_type: str = None):
#     logger.info("Starting metrics server.")
#     start_http_server(settings.METRICS_PORT, settings.METRICS_ADDRESS)
#
#     logger.info(f"Worker is a {worker_type}.")
#
#     while True:
#         with session_factory() as session:
#             logger.info("Starting rewards cron")
#
#             # build_methods(session)
#             build_volumes(session)
#
#             prom_metrics.crons_ran.inc()
#             logger.info("Sleeping after crons.")
#             sleep(settings.CRON_SLEEP_SEC)


if __name__ == '__main__':
    # TODO: When enabling stream processing, uncomment this
    # import argparse
    #
    # parser = argparse.ArgumentParser(description="Worker type input.")
    # parser.add_argument("worker_type", type=str, help="The type of worker", default="")
    # args = parser.parse_args()
    # main(args.worker_type)
    main()
