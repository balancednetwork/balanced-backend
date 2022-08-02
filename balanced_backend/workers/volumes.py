import datetime
from datetime import timezone

from typing import TYPE_CHECKING
from sqlmodel import select

from balanced_backend.log import logger
from balanced_backend.metrics import prom_metrics
from balanced_backend.utils.time_to_block import get_block_from_timestamp
from balanced_backend.utils.api import get_logs_in_blocks
from balanced_backend.utils.values import get_total_indexed

from balanced_backend.models.volumes_base import VolumeIntervalBase
from balanced_backend.tables.volumes import ContractMethodVolume
from balanced_backend.workers.volumes_addresses import daily_volumes

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def set_table_value_from_time_period(
        session: 'Session',
        context: 'VolumeIntervalBase',
):
    block_start = get_block_from_timestamp(int(context.start_timestamp * 1e6))
    block_end = get_block_from_timestamp(int(context.end_timestamp * 1e6))

    events = get_logs_in_blocks(
        address=context.address,
        method=context.method,
        block_start=block_start,
        block_end=block_end-1,
    )

    value = 0
    num_events = 0

    if events is not None:
        try:
            value = get_total_indexed(
                events=events,
                indexed_position=context.indexed_position,
                decimals=context.decimals,
            )
        except IndexError as e:
            logger.info(f"Error processing "
                        f"address={context.address} "
                        f"method={context.method} "
                        f"indexed_position={context.indexed_position} "
                        f"block_start=block_start ",
                        f"block_end={block_end - 1} ",
                        f"events={events}")
            raise e
        num_events = len(events)

        # Metrics
    prom_metrics.crons_last_timestamp = datetime.datetime.now().timestamp()
    prom_metrics.crons_ran.inc()

    # Update things like days since launch
    context.update_time()

    model = ContractMethodVolume(
        **context.dict(),
        value=value,
        start_date=datetime.datetime.utcfromtimestamp(context.start_timestamp),
        end_date=datetime.datetime.utcfromtimestamp(context.end_timestamp),
        start_block=block_start,
        end_block=block_end,
        num_events=num_events,
    )
    logger.info(f"Inserting value {value} into {ContractMethodVolume.__tablename__} for time "
                f"{datetime.datetime.fromtimestamp(context.end_timestamp)}.")
    session.merge(model)
    session.commit()


def init_time_series(
        session: 'Session',
        context: 'VolumeIntervalBase',
):
    """
    Iterate through timestamps from start time every day.
    Start time: Loans contract started April 25, 2021 -> 1619308800
    """
    now = datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()

    # Here we want to start the timestamps so that they fall exactly at 12 AM UTC
    year = datetime.date.fromtimestamp(context.init_chart_time).year
    month = datetime.date.fromtimestamp(context.init_chart_time).month
    day = datetime.date.fromtimestamp(context.init_chart_time).day
    dt = datetime.datetime(year, month, day)

    context.start_timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
    context.end_timestamp = context.start_timestamp + context.update_interval

    while now > context.end_timestamp:
        set_table_value_from_time_period(
            session=session,
            context=context,
        )
        # Add interval
        context.end_timestamp += context.update_interval
        context.start_timestamp += context.update_interval


def build_volumes_time_series(
        session: 'Session',
        context: 'VolumeIntervalBase',
):
    """
    Run on a cron, this function first checks if we need to update the loans_chart table
     then if the value is within the min_update_time,
    :return:
    """
    time_series = session.execute(
        select(ContractMethodVolume)
            .where(ContractMethodVolume.address == context.address)
            .where(ContractMethodVolume.method == context.method)
            .order_by(ContractMethodVolume.end_timestamp.desc())
    ).scalars().all()

    # Calc last updated time
    if len(time_series) > 0:
        last_updated_time = time_series[0].end_timestamp
    else:
        # We have an empty DB -> init
        logger.info(f"{ContractMethodVolume.__tablename__} empty - initializing.")
        init_time_series(
            session=session,
            context=context,
        )
        logger.info(f"{ContractMethodVolume.__tablename__} - initialized.")
        return

    now = datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()
    diff_last_updated_time = now - last_updated_time

    if diff_last_updated_time < context.update_interval:
        logger.info(f"Already updated {context.address} / {context.method} at "
                    f"{last_updated_time}")
        return

    num_updates = int(round(diff_last_updated_time / context.update_interval, 0))
    for i in range(1, num_updates + 1):

        context.end_timestamp = int(last_updated_time + i * context.update_interval)
        context.start_timestamp = context.end_timestamp - context.update_interval
        context.update_time()

        set_table_value_from_time_period(
            session=session,
            context=context,
        )


def build_volumes(
        session: 'Session',
):
    for i in daily_volumes:
        context = VolumeIntervalBase(**i)

        context.init_model()
        context.update_interval = 24 * 60 * 60

        build_volumes_time_series(
            session=session,
            context=context,
        )

        print()
