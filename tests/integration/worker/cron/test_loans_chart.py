from balanced_backend.workers.crons.loans_chart import get_loans_chart, \
    init_loans_chart, get_loans_chart_data_point


def test_get_loans_chart_data_point_valid():
    """Method exists at this time."""
    loans_value = get_loans_chart_data_point(1654409623 * 1000000)
    assert round(loans_value, 0) == 30976667.0


def test_get_loans_chart_data_point_invalid():
    """Method does not exist at this time."""
    loans_value = get_loans_chart_data_point(1619308800 * 1000000)
    assert loans_value is None


def test_init_loans_chart():
    init_loans_chart


def test_get_loans_chart(db):
    get_loans_chart(db)
