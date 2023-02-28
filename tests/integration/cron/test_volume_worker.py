import datetime

import pytest
from freezegun import freeze_time
from sqlmodel import select

from balanced_backend.tables.volumes import ContractMethodVolume
from balanced_backend.cron.volumes import (
    set_table_value_from_time_period,
    build_volumes_time_series
)


@pytest.mark.order(1)
@freeze_time("2022-06-22")
def test_build_daily_volumes(db, loans_feepaid_volumes_context):
    """Validate indexed event log events."""
    # Change update interval so it only does one update
    loans_feepaid_volumes_context.start_timestamp = 1655723172
    loans_feepaid_volumes_context.init_chart_time = 1655723172
    loans_feepaid_volumes_context.update_time()

    with db as session:
        build_volumes_time_series(
            session=session,
            context=loans_feepaid_volumes_context,
        )
        result = session.execute(
            select(ContractMethodVolume).where(
                ContractMethodVolume.address == loans_feepaid_volumes_context.address)).scalars().all()
        print(result)
        assert result


@pytest.mark.order(1)
@freeze_time("2021-09-07")
def test_build_daily_volumes_rebalance(db, loans_rebalance_volumes_context):
    """Validate events that are non-indexed."""
    # Change update interval so it only does one update
    context = loans_rebalance_volumes_context
    context.init_model()
    # context.update_time()

    with db as session:
        build_volumes_time_series(
            session=session,
            context=context,
        )
        result = session.execute(
            select(ContractMethodVolume).where(
                ContractMethodVolume.address == context.address)).scalars().all()
        print(result)
        assert result


@pytest.mark.order(1)
def test_set_table_value_from_time_period(db, loans_feepaid_volumes_context):
    with db as session:
        loans_feepaid_volumes_context.init_model()

        loans_feepaid_volumes_context.start_timestamp = 1655830839
        loans_feepaid_volumes_context.end_timestamp = 1655840625

        set_table_value_from_time_period(
            session=session,
            context=loans_feepaid_volumes_context,
        )
