from typing import TYPE_CHECKING

from balanced_backend.utils.historical import build_interval_time_series
from balanced_backend.workers.daily_historical_addresses import daily_historical
from balanced_backend.models.historical import DailyHistorical
from balanced_backend.models.historical_base import HistoricalMethodInterval

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def build_daily_historical(
        session: 'Session',
):
    for i in daily_historical:

        historical_method_interval = HistoricalMethodInterval(**i)
        historical_method_interval.init_model()
        historical_method_interval.update_interval = 24 * 60 * 60
        build_interval_time_series(
            session=session,
            context=historical_method_interval,
        )

        print()

