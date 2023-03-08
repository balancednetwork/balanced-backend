from typing import TYPE_CHECKING
from loguru import logger

from balanced_backend.utils.methods import build_interval_time_series
from balanced_backend.cron.method_addresses import contract_methods
from balanced_backend.models.contract_method_base import ContractMethodBase

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def run_methods(
        session: 'Session',
):
    logger.info("Running methods cron...")
    for i in contract_methods:
        historical_method_interval = ContractMethodBase(**i)
        historical_method_interval.init_model()
        historical_method_interval.update_interval = 24 * 60 * 60
        build_interval_time_series(
            session=session,
            context=historical_method_interval,
        )
    logger.info("Ending methods cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_methods(session=session)
