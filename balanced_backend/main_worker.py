from time import sleep
from loguru import logger
from prometheus_client import start_http_server

from balanced_backend.config import settings
from balanced_backend.db import session_factory
from balanced_backend.metrics import prom_metrics

from balanced_backend.workers.methods import build_methods
from balanced_backend.workers.volumes import build_volumes


def main(worker_type: str = None):
    logger.info("Starting metrics server.")
    start_http_server(settings.METRICS_PORT, settings.METRICS_ADDRESS)

    logger.info(f"Worker is a {worker_type}.")

    while True:
        with session_factory() as session:
            logger.info("Starting rewards cron")

            build_methods(session)
            build_volumes(session)

            prom_metrics.crons_ran.inc()
            logger.info("Sleeping after crons.")
            sleep(settings.CRON_SLEEP_SEC)


if __name__ == '__main__':
    # TODO: When enabling stream processing, uncomment this
    # import argparse
    #
    # parser = argparse.ArgumentParser(description="Worker type input.")
    # parser.add_argument("worker_type", type=str, help="The type of worker", default="")
    # args = parser.parse_args()
    # main(args.worker_type)
    main()
