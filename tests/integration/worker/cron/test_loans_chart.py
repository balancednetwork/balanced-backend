from sqlmodel import select

from balanced_backend.models.loans_chart import LoansChart
from balanced_backend.workers.crons.loans_chart import get_loans_chart, \
    set_loans_chart_from_timestamp, get_loans_chart_data_point


def test_get_loans_chart_data_point_valid():
    """Method exists at this time."""
    loans_value = get_loans_chart_data_point(1654409623 * 1000000)
    assert round(loans_value, 0) == 30976667.0


def test_get_loans_chart_data_point_invalid():
    """Method does not exist at this time."""
    loans_value = get_loans_chart_data_point(1619308800 * 1000000)
    assert loans_value is None


def test_set_loans_chart_from_timestamp(db):
    """Check that we can idepotently update the DB with values at a given timestamp."""
    timestamp = 1654409623
    assert set_loans_chart_from_timestamp(db, timestamp * 1000000)
    with db as session:
        result = session.execute(
            select(LoansChart).where(LoansChart.timestamp == timestamp))
        loans = result.scalars().all()
        assert loans[0].timestamp == timestamp


def test_get_loans_chart(db):
    get_loans_chart(db)
