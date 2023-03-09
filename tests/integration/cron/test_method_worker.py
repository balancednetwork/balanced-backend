import pytest
from freezegun import freeze_time
from sqlmodel import select

from balanced_backend.cron.methods import run_methods
from balanced_backend.tables.historical import DailyHistorical
from balanced_backend.utils.methods import set_table_value_from_timestamp


@pytest.mark.order(1)
def test_set_table_value_from_timestamp(db, loans_historical_context):
    """Check that we can idepotently update the DB with values at a given timestamp."""
    loans_historical_context.init_model()

    set_table_value_from_timestamp(db, context=loans_historical_context)
    with db as session:
        result = session.execute(
            select(DailyHistorical).where(
                DailyHistorical.timestamp == loans_historical_context.timestamp))
        loans = result.scalars().all()
        assert loans[0].timestamp == loans_historical_context.timestamp


# @pytest.mark.order(1)
# @freeze_time("2021-04-26")
# def test_build_daily_historical(db):
#     with db as session:
#         run_methods(session=session)
