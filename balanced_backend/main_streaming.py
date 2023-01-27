from loguru import logger
from prometheus_client import start_http_server

from balanced_backend.config import settings
from balanced_backend.db import session_factory
from balanced_backend.streaming.consumer import Processor


def main():
    logger.info("Starting metrics server.")
    start_http_server(settings.METRICS_PORT, settings.METRICS_ADDRESS)
    with session_factory() as session:
        kafka = Processor(session=session)
        kafka.start()


if __name__ == '__main__':
    main()
