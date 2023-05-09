from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from balanced_backend.db import get_session
from balanced_backend.tables.pools import Pool
from balanced_backend.tables.series import PoolSeriesTableType
from balanced_backend.tables.dividends import Dividend
# from balanced_backend.cron.pool_volumes_series import get_table
from balanced_backend.tables.utils import get_pool_series_table
from balanced_backend.config import settings

router = APIRouter()


@router.get("/pools")
async def get_pools(
        response: Response,
        session: AsyncSession = Depends(get_session),
        base_address: str = None,
        quote_address: str = None,
        base_symbol: str = None,
        quote_symbol: str = None,
        pool_id: int = None,
        name: str = None,
        type: str = None,
) -> Union[List[Pool], Response]:
    """Return list of pools."""
    if pool_id and name:
        raise HTTPException(
            status_code=400,
            detail="Can only specify `pool_id` or `name`, not both."
        )

    if (pool_id or name) and \
            (quote_address or quote_symbol or base_address or quote_address):
        raise HTTPException(
            status_code=400,
            detail="Doesn't make sense to specify `pool_id` or `name`, with additional "
                   "parameters. Check your query."
        )

    query = select(Pool)

    if name is not None:
        query = query.where(Pool.name == name)
    elif pool_id is not None:
        query = query.where(Pool.pool_id == pool_id)
    else:
        if base_address is not None:
            query = query.where(Pool.base_address == base_address)
        if quote_address is not None:
            query = query.where(Pool.quote_address == quote_address)
        if base_symbol is not None:
            query = query.where(Pool.base_symbol == base_symbol)
        if quote_symbol is not None:
            query = query.where(Pool.quote_symbol == quote_symbol)

    if type is not None:
        if type not in ['community', 'balanced']:
            raise HTTPException(
                status_code=400,
                detail="Parameter `type` must be one of 'community' or 'balanced'"
            )
        query = query.where(Pool.type == type)

    result = await session.execute(query)
    pools: list[Pool] = result.scalars().all()

    # Check if exists
    if len(pools) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)  # noqa

    # Return the count in header
    total_count = str(len(pools))
    response.headers["x-total-count"] = total_count

    return pools


INTERVAL_MAP = {
    "5m": {
        "table_name": "5Min",
        "seconds": 60 * 5,
    },
    "15m": {
        "table_name": "15Min",
        "seconds": 60 * 15,
    },
    "1h": {
        "table_name": "1Hour",
        "seconds": 60 * 60,
    },
    "4h": {
        "table_name": "4Hour",
        "seconds": 60 * 60 * 4,
    },
    "1d": {
        "table_name": "1Day",
        "seconds": 86400,
    },
    "1w": {
        "table_name": "1Week",
        "seconds": 86400 * 7,
    },
}
INTERVALS = {k for k, _ in INTERVAL_MAP.items()}


@router.get("/pools/series/{pool_id}/{interval}/{start}/{end}")
async def get_pools_series(
        response: Response,
        session: AsyncSession = Depends(get_session),
        pool_id: int = None,
        interval: str = None,
        start: int = None,
        end: int = None,
) -> Union[List[PoolSeriesTableType], Response]:
    """Return list of pools price/volumes time series."""

    if interval not in INTERVALS:
        raise HTTPException(
            status_code=400,
            detail=f"Interval must be one of {', '.join([i for i in INTERVALS])}."
        )

    num_records = (end - start) / INTERVAL_MAP[interval]['seconds']
    if num_records > settings.MAX_TS_RECORDS:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum of {settings.MAX_TS_RECORDS} returned. Attempting to get "
                   f"{num_records}..."
        )

    table = get_pool_series_table(table_suffix=INTERVAL_MAP[interval]['table_name'])

    query = select(table).where(
        table.chain_id == settings.CHAIN_ID,
        table.timestamp >= start,
        table.timestamp <= end,
        table.pool_id == pool_id,
    )

    query = query.order_by(table.timestamp.asc())

    result = await session.execute(query)
    timeseries: list[table] = result.scalars().all()

    # Check if exists
    if len(timeseries) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)  # noqa

    # Return the count in header
    total_count = str(len(timeseries))
    response.headers["x-total-count"] = total_count

    return timeseries


@router.get("/pools/dividends")
async def pools_dividends(
        response: Response,
        session: AsyncSession = Depends(get_session),
        pool_id: int = None,
        base_address: str = None,
        quote_address: str = None,
) -> Union[List[Dividend], Response]:
    """Return list of pool dividends."""

    query = select(Dividend).where(Dividend.chain_id == settings.CHAIN_ID)

    if pool_id is not None:
        query.where(Dividend.pool_id >= pool_id)
    if quote_address is not None:
        query.where(Dividend.quote_address >= quote_address)
    if base_address is not None:
        query.where(Dividend.base_address >= base_address)

    result = await session.execute(query)
    dividends: list[Dividend] = result.scalars().all()

    # Check if exists
    if len(dividends) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)  # noqa

    # Return the count in header
    total_count = str(len(dividends))
    response.headers["x-total-count"] = total_count

    return dividends
