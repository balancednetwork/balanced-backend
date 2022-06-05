from time import sleep

from loguru import logger
from prometheus_client import start_http_server

from balanced_backend.config import settings
from balanced_backend.db import session_factory
from balanced_backend.metrics import prom_metrics
from balanced_backend.workers.crons.loans_chart import get_loans_chart


def main(worker_type: str = None):
    logger.info("Starting metrics server.")
    start_http_server(settings.METRICS_PORT, settings.METRICS_ADDRESS)

    logger.info(f"Worker is a {worker_type}.")

    if worker_type == "cron":
        while True:
            with session_factory() as session:
                logger.info("Starting rewards cron")
                get_loans_chart(session)
                prom_metrics.rewards_cron_ran.inc()

                logger.info("Sleeping after crons.")
                sleep(settings.CRON_SLEEP_SEC)
