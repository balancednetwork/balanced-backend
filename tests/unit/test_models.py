from balanced_backend.models.historical import DailyHistorical


def test_historical_model_datetime(db):
    h = DailyHistorical(
        address="hxFOO",
        timestamp=1655041939,
    )
    assert h
