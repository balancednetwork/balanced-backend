from sqlmodel import select
from typing import List, Union, TYPE_CHECKING
from datetime import datetime

from balanced_backend.metrics import prom_metrics
from balanced_backend.models.loans_chart import LoansChart
from balanced_backend.utils.rpc import loans_getTotalCollateral, convert_hex_int
from balanced_backend.utils.time_to_block import get_block_from_timestamp
from balanced_backend.log import logger

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_loans_chart_data_point(timestamp: int = None) -> Union[float, None]:
    """Get the loans contract TotalCollateral from timestamp."""
    height = get_block_from_timestamp(timestamp=timestamp)
    if height == 0:
        return

    r = loans_getTotalCollateral(height=height)
    if r.status_code == 200:
        loans_amount = r.json()['result']
        return convert_hex_int(loans_amount) / 1e18
    else:
        logger.info("Invalid response to get_loans_amount. Contract may not have "
                    "method then.")
        return


def set_loans_chart_from_timestamp(session: 'Session', loan_time: int) -> bool:
    loans_amount = get_loans_chart_data_point(int(loan_time * 1e6))

    if loans_amount is not None:
        loans_chart = LoansChart(
            timestamp=int(loan_time),
            datetime=datetime.fromtimestamp(loan_time),
            value=loans_amount
        )
        logger.info(f"Inserting value {loans_amount} for time {datetime.fromtimestamp(loan_time)}.")
        session.merge(loans_chart)
        session.commit()
        return True
    else:
        logger.info(f"Loans contract likely does not have the method at this time, ie "
                    f"{datetime.fromtimestamp(loan_time)}, or an API is down.")
        return False


def init_loans_chart(session: 'Session'):
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


def get_loans_chart(session: 'Session'):
    """
    Run on a cron, this function first checks if we need to update the loans_chart table
     then if the value is within the min_update_time,
    :return:
    """
    loans_time_series: List[LoansChart] = session.execute(
        select(LoansChart).order_by(LoansChart.timestamp.desc())).scalars().all()

    # Calc last updated time
    if len(loans_time_series) > 0:
        last_updated_time = loans_time_series[0].timestamp
    else:
        # We have an empty DB -> init
        logger.info("loans chart empty - initializing.")
        init_loans_chart(session)
        logger.info("loans chart empty - initialized.")
        return

    # Condition we have data in DB but could be producing another data point
    diff_last_updated_time = datetime.now().timestamp() - last_updated_time
    if diff_last_updated_time > 60 * 60 * 24:
        num_updates = int(round(diff_last_updated_time / 60 / 60 / 24, 0))
        for i in range(1, num_updates + 1):
            update_time = 60 * 60 * 24 * i + last_updated_time
            loans_amount = get_loans_chart_data_point(int(update_time * 1e6))

            if loans_amount is None:
                logger.info(
                    "Could not get loans amount, endpoint not reachable most likely.")

            prom_metrics.crons_last_timestamp = datetime.now().timestamp()
            prom_metrics.crons_ran.inc()

            loans_chart = LoansChart(
                timestamp=update_time,
                datetime=datetime.fromtimestamp(update_time),
                value=loans_amount
            )
            session.merge(loans_chart)
            session.commit()
            return
    else:
        logger.info(f"Last updated {datetime.fromtimestamp(last_updated_time)}, next "
                    f"update in {diff_last_updated_time} seconds")

