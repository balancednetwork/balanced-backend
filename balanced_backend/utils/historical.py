from datetime import datetime
from typing import List, Union, TYPE_CHECKING, Callable, Type
from sqlmodel import SQLModel, select

from balanced_backend.log import logger
from balanced_backend.metrics import prom_metrics
from balanced_backend.utils.time_to_block import get_block_from_timestamp
from balanced_backend.utils.rpc import convert_hex_int

if TYPE_CHECKING:
    from sqlalchemy.orm import Session
    from sqlmodel import SQLModel


def get_value_from_timestamp(
        timestamp: int,
        rpc_call: Callable,
) -> Union[float, None]:
    """Get the loans contract TotalCollateral from timestamp."""
    height = get_block_from_timestamp(timestamp=timestamp)
    if height == 0:
        logger.info("Error getting block from timestamp.")
        return

    r = rpc_call(height=height)
    if r.status_code == 200:
        loans_amount = r.json()['result']
        return convert_hex_int(loans_amount) / 1e18
    else:
        logger.info("Invalid response to get_loans_amount. Contract may not have "
                    "method then.")
        return


def set_table_value_from_timestamp(
        session: 'Session',
        rpc_call: Callable,
        Model: Type[SQLModel],
        rpc_time: int,
) -> bool:
    value = get_value_from_timestamp(
        timestamp=int(rpc_time * 1e6),
        rpc_call=rpc_call,
    )

    if value is not None:
        model = Model(
            timestamp=int(rpc_time),
            datetime=datetime.fromtimestamp(rpc_time),
            value=value
        )
        logger.info(f"Inserting value {value} into {Model.__tablename__} for time "
                    f"{datetime.fromtimestamp(rpc_time)}.")
        session.merge(model)
        session.commit()
        return True
    else:
        logger.info(f"{rpc_call.__name__} likely does not have the method at this time,"
                    f" ie {datetime.fromtimestamp(rpc_time)}, or an API is down.")
        return False


def init_time_series(
        session: 'Session',
        rpc_call: Callable,
        Model: Type[SQLModel],
        init_chart_time: int,
):
    """
    Iterate through timestamps from start time every day.
    Start time: Loans contract started April 25, 2021 -> 1619308800
    """
    now = datetime.now().timestamp()
    rpc_time = init_chart_time
    while now > rpc_time:
        set_table_value_from_timestamp(
            session=session,
            rpc_call=rpc_call,
            Model=Model,
            rpc_time=rpc_time,
        )
        # Add a day
        rpc_time += 60 * 60 * 24


def build_time_series(
        session: 'Session',
        rpc_call: Callable,
        Model: Type[SQLModel],
        init_chart_time: int,
):
    """
    Run on a cron, this function first checks if we need to update the loans_chart table
     then if the value is within the min_update_time,
    :return:
    """
    time_series: List[Model] = session.execute(
        select(Model).order_by(Model.timestamp.desc())).scalars().all()

    # Calc last updated time
    if len(time_series) > 0:
        last_updated_time = time_series[0].timestamp
    else:
        # We have an empty DB -> init
        logger.info(f"{Model.__tablename__} empty - initializing.")
        init_time_series(
            session=session,
            rpc_call=rpc_call,
            Model=Model,
            init_chart_time=init_chart_time,
        )
        logger.info(f"{Model.__tablename__} - initialized.")
        return

    # Condition we have data in DB but could be producing another data point
    diff_last_updated_time = datetime.now().timestamp() - last_updated_time
    if diff_last_updated_time > 60 * 60 * 24:
        num_updates = int(round(diff_last_updated_time / 60 / 60 / 24, 0))
        for i in range(1, num_updates + 1):
            update_time = 60 * 60 * 24 * i + last_updated_time
            loans_amount = get_value_from_timestamp(int(update_time * 1e6))

            if loans_amount is None:
                logger.info(
                    "Could not get loans amount, endpoint not reachable most likely.")

            prom_metrics.crons_last_timestamp = datetime.now().timestamp()
            prom_metrics.crons_ran.inc()

            model = Model(
                timestamp=update_time,
                datetime=datetime.fromtimestamp(update_time),
                value=loans_amount
            )
            session.merge(model)
            session.commit()
            return
    else:
        logger.info(f"Last updated {datetime.fromtimestamp(last_updated_time)}, next "
                    f"update in {diff_last_updated_time} seconds.")
