from sqlmodel import select
from typing import List, Union, TYPE_CHECKING
from datetime import datetime

from balanced_backend.config import settings
from balanced_backend.metrics import prom_metrics
from balanced_backend.models.loans_chart import LoansChart
from balanced_backend.utils.rpc import get_loans_amount, convert_hex_int
from balanced_backend.utils.time_to_block import get_block_from_timestamp
from balanced_backend.log import logger

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_loans_chart_data_point(timestamp: int = None) -> Union[float, None]:
    """Get the loans contract TotalCollateral from timestamp."""
    height = get_block_from_timestamp(timestamp=timestamp)
    if height == 0:
        return

    r = get_loans_amount(height=height)
    if r.status_code == 200:
        loans_amount = r.json()['result']
        return convert_hex_int(loans_amount) / 1e18
    else:
        logger.info("Invalid response to get_loans_amount. Contract may not have "
                    "method then.")
        return


def set_loans_chart_from_timestamp(session: Session, loan_time: int) -> bool:
    loans_amount = get_loans_chart_data_point(loan_time * 1000)

    if loans_amount is not None:
        loans_chart = LoansChart(
            timestamp=int(loan_time / 1e6),
            value=loans_amount
        )

        session.merge(loans_chart)
        session.commit()
        return True
    else:
        logger.info("Loans contract likely does not have the method at this time "
                    "or an API is down.")
        return False


def init_loans_chart(session: Session):
    """
    Iterate through timestamps from start time every day.
    Start time: Loans contract started April 25, 2021 -> 1619308800
    """
    now = datetime.now().timestamp()
    loan_time = 1619308800
    while now > loan_time:
        set_loans_chart_from_timestamp(session, loan_time)
        # Add a day
        loan_time += 60 * 60 * 24


def get_loans_chart(session):
    """
    Run on a cron, this function first checks if we need to update the loans_chart table
     then if the value is within the min_update_time,
    :return:
    """
    loans_time_series: List[LoansChart] = session.execute(
        select(LoansChart).order_by(LoansChart.timestamp)).scalars().all()

    # Calc last updated time
    if len(loans_time_series) > 0:
        last_updated_time = loans_time_series[0].timestamp
    else:
        # We have an empty DB -> init
        logger.info("loans chart empty - initializing.")
        init_loans_chart(session)
        return

    if last_updated_time + 3600 * 1000 * settings.LOANS_CHART_MIN_TIME_STEP_MIN < datetime.now().timestamp():
        prom_metrics.crons_last_timestamp = datetime.now().timestamp()
        prom_metrics.crons_ran.inc()
        loans_amount = get_loans_chart_data_point()
    else:
        return

    if loans_amount is None:
        logger.info("Could not get loans amount, endpoint not reachable most likely.")

    loans_chart = LoansChart(
        timestamp=datetime.now().timestamp(),
        value=loans_amount
    )

    session.merge(loans_chart)
    session.commit()
