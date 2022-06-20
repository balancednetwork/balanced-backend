from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from balanced_backend.db import engine
from balanced_backend.models.historical_base import HistoricalMethodInterval


@pytest.fixture(scope="session")
def db():
    SessionMade = sessionmaker(bind=engine)
    session = SessionMade()

    yield session


@pytest.fixture(scope="module")
def client() -> Generator:
    from balanced_backend.main_api import app

    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def loans_context():
    context = HistoricalMethodInterval(
        timestamp=1625745538,
        params={
            "to": "cx66d4d90f5f113eba575bf793570135f9b10cece1",
            "dataType": "call",
            "data": {"method": "getTotalCollateral"}
        },
        init_chart_time=1619308800,
        update_interval=1000000000,
    )
    return context
