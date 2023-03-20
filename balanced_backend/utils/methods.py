from datetime import datetime
from typing import Union, TYPE_CHECKING
from sqlmodel import select

from balanced_backend.log import logger
from balanced_backend.metrics import prom_metrics
from balanced_backend.tables.historical import DailyHistorical
from balanced_backend.models.contract_method_base import ContractMethodBase
from balanced_backend.utils.time_to_block import get_block_from_timestamp
from balanced_backend.utils.rpc import convert_hex_int, get_icx_call_block_height

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_value_from_timestamp(
        context: 'ContractMethodBase',
) -> Union[float, None]:
    """Get the loans contract TotalCollateral from timestamp."""
    height = get_block_from_timestamp(timestamp=int(context.timestamp * 1e6))
    if height == 0:
        logger.info("Error getting block from timestamp.")
        return

    r = get_icx_call_block_height(params=context.params.dict(), height=height)
    if r.status_code == 200:
        loans_amount = r.json()['result']
        return convert_hex_int(loans_amount) / 10 ** context.decimals
    else:
        logger.info("Invalid response to get_loans_amount. Contract may not have "
                    "method then.")
        return


def set_table_value_from_timestamp(
        session: 'Session',
        context: 'ContractMethodBase',
):
    value = get_value_from_timestamp(context=context)

    if value is not None:
        context.update_time()

        model = DailyHistorical(**context.dict(), value=value)
        logger.info(f"Inserting value {value} into {DailyHistorical.__tablename__} for time "
                    f"{datetime.fromtimestamp(context.timestamp)}.")
        session.merge(model)
        session.commit()


def init_time_series(
        session: 'Session',
        context: 'ContractMethodBase',
):
    """
    Iterate through timestamps from start time every day.
    Start time: Loans contract started April 25, 2021 -> 1619308800
    """
    now = datetime.now().timestamp()
    context.timestamp = context.init_chart_time
    while now > context.timestamp:
        set_table_value_from_timestamp(
            session=session,
            context=context,
        )
        # Add interval
        context.timestamp += context.update_interval


def build_interval_time_series(
        session: 'Session',
        context: 'ContractMethodBase',
):
    """
    Run on a cron, this function first checks if we need to update the loans_chart table
     then if the value is within the min_update_time,
    :return:
    """
    time_series = session.execute(
        select(DailyHistorical)
            .where(DailyHistorical.address == context.address)
            .where(DailyHistorical.contract_name == context.contract_name)
            .where(DailyHistorical.method == context.method)
            .order_by(DailyHistorical.timestamp.desc())
    ).scalars().all()

    # Calc last updated time
    if len(time_series) > 0:
        last_updated_time = time_series[0].timestamp
    else:
        # We have an empty DB -> init
        logger.info(f"{DailyHistorical.__tablename__} empty - initializing.")
        init_time_series(
            session=session,
            context=context,
        )
        logger.info(f"{DailyHistorical.__tablename__} - initialized.")
        return

    # Condition we have data in DB but could be producing another data point
    diff_last_updated_time = datetime.now().timestamp() - last_updated_time
    if diff_last_updated_time > context.update_interval:
        num_updates = int(round(diff_last_updated_time / context.update_interval, 0))
        for i in range(1, num_updates + 1):
            context.timestamp = context.update_interval * i + last_updated_time
            context.update_time()
            value = get_value_from_timestamp(context=context)

            if value is None:
                raise Exception(
                    "Could not get value amount, endpoint not reachable most likely.")

            # Metrics
            prom_metrics.crons_last_timestamp = datetime.now().timestamp()
            prom_metrics.crons_ran.inc()

            model = DailyHistorical(**context.dict(), value=value)
            session.merge(model)
            session.commit()
    else:
        logger.info(f"Last updated {datetime.fromtimestamp(last_updated_time)}, next "
                    f"update in {diff_last_updated_time} seconds.")
