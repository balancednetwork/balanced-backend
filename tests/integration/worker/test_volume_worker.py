import datetime

import pytest
from freezegun import freeze_time
from sqlmodel import select

from balanced_backend.tables.volumes import ContractMethodVolume
from balanced_backend.workers.volumes import (
    set_table_value_from_time_period,
    build_volumes_time_series
)


# @pytest.mark.first
# @freeze_time("2022-06-22")
# def test_build_daily_volumes(db, loans_volumes_context):
#     # Change update interval so it only does one update
#     loans_volumes_context.start_timestamp = 1655723172
#     loans_volumes_context.init_chart_time = 1655723172 - 86400
#     loans_volumes_context.update_time()
#     # 1655769600
# 
#     with db as session:
#         build_volumes_time_series(
#             session=session,
#             context=loans_volumes_context,
#         )
#         result = session.execute(
#             select(ContractMethodVolume).where(
#                 ContractMethodVolume.address == loans_volumes_context.address)).scalars().all()
#         assert result


def test_set_table_value_from_time_period(db, loans_volumes_context):
    with db as session:
        loans_volumes_context.init_model()

        loans_volumes_context.start_timestamp = 1655830839
        loans_volumes_context.end_timestamp = 1655840625

        set_table_value_from_time_period(
            session=session,
            context=loans_volumes_context,
        )
