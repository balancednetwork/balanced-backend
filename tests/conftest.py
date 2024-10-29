import asyncio
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
    SessionMade = sessionmaker(bind=engine, autoflush=False)
    session = SessionMade()

    yield session


@pytest.fixture()
def db_migration():
    import alembic.config

    cur_dir = os.path.abspath(os.path.dirname(__file__))
    alembic_dir = os.path.join(cur_dir, "../../balanced_backend")
    os.chdir(alembic_dir)

    alembicArgs = [
        "--raiseerr",
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=alembicArgs)
    yield

    # from balanced_backend.alembic.env import run_migrations_offline
    # run_migrations_offline()

@pytest.yield_fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client(event_loop) -> TestClient:
    from balanced_backend.main_api import app

    return TestClient(app)


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
        address="",
        method="",
        contract_name="",
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
