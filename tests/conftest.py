from typing import Generator
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from balanced_backend.db import engine
from balanced_backend.models.contract_method_base import ContractMethodBase, Params
from balanced_backend.models.volumes_base import VolumeIntervalBase


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


@pytest.fixture(scope='function')
def get_fixture(request):
    """Get the fixtures dir in the current directory of the test."""
    def f(fixture_name):
        return os.path.join(request.fspath.dirname, 'fixtures', fixture_name)
    return f


@pytest.fixture(scope="function")
def loans_historical_context():
    context = ContractMethodBase(
        timestamp=1625745538,
        params=Params(**{
            "to": "cx66d4d90f5f113eba575bf793570135f9b10cece1",
            "dataType": "call",
            "data": {"method": "getTotalCollateral"}
        }),
        init_chart_time=1619308800,
        update_interval=1000000000,
    )
    return context


@pytest.fixture(scope="function")
def loans_feepaid_volumes_context():
    context = VolumeIntervalBase(
        # timestamp=1625745538,
        address="cx66d4d90f5f113eba575bf793570135f9b10cece1",
        contract_name="loans",
        indexed_position=1,
        method='FeePaid',
        init_chart_time=1619308800,
        update_interval=86400,
    )
    return context


@pytest.fixture(scope="function")
def loans_rebalance_volumes_context():
    context = VolumeIntervalBase(
        # timestamp=1625745538,
        address="cx66d4d90f5f113eba575bf793570135f9b10cece1",
        contract_name="loans",
        indexed_position=1,
        method='Rebalance',
        init_chart_block=39340509,
        update_interval=86400,
    )
    return context
