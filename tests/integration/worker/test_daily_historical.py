import pytest
from freezegun import freeze_time
from sqlmodel import select

from balanced_backend.workers.daily_historical import build_daily_historical
from balanced_backend.models.historical import DailyHistorical

from balanced_backend.utils.historical import set_table_value_from_timestamp


@pytest.mark.first
def test_set_table_value_from_timestamp(db, loans_context):
    """Check that we can idepotently update the DB with values at a given timestamp."""
    loans_context.init_model()

    set_table_value_from_timestamp(db, context=loans_context)
    with db as session:
        result = session.execute(
            select(DailyHistorical).where(
                DailyHistorical.timestamp == loans_context.timestamp))
        loans = result.scalars().all()
        assert loans[0].timestamp == loans_context.timestamp


@freeze_time("2021-04-26")
def test_build_daily_historical(db):
    with db as session:
        build_daily_historical(session=session)
