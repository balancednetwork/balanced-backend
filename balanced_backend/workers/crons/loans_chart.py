from sqlmodel import select
from typing import List
from datetime import datetime

from balanced_backend.config import settings
from balanced_backend.metrics import prom_metrics
from balanced_backend.models.loans_chart import LoansChart


def init_loans_chart(timestamp: int):
    pass


def get_loans_chart_data_point(timestamp: int = None):
    pass


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
        last_updated_time = 0  # We have an empty DB -> proceed

    if last_updated_time + 3600 * 1000 * settings.LOANS_CHART_MIN_TIME_STEP_MIN > datetime.now().timestamp():
        prom_metrics.crons_last_timestamp = datetime.now().timestamp()
        prom_metrics.crons_ran.inc()
        loans_amount = get_loans_chart_data_point()
    else:
        return


