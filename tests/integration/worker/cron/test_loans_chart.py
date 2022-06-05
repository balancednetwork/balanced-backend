from balanced_backend.workers.crons.loans_chart import get_loans_chart


def test_get_loans_chart(db):
    get_loans_chart(db)
