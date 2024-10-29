from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from balanced_backend.db import get_session
from balanced_backend.tables.pools import Pool
from balanced_backend.tables.series import PoolSeriesTableType, PoolSeriesBase
from balanced_backend.tables.dividends import Dividend
from balanced_backend.tables.utils import get_pool_series_table, get_token_series_table
from balanced_backend.config import settings

router = APIRouter()


@router.get("/pools", response_model=List[Pool])
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
            status_code=400, detail="Can only specify `pool_id` or `name`, not both."
        )

    if (pool_id or name) and (
        quote_address or quote_symbol or base_address or quote_address
    ):
        raise HTTPException(
            status_code=400,
            detail="Doesn't make sense to specify `pool_id` or `name`, with additional "
            "parameters. Check your query.",
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
        if type not in ["community", "balanced"]:
            raise HTTPException(
                status_code=400,
                detail="Parameter `type` must be one of 'community' or 'balanced'",
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


@router.get(
    "/pools/series/{pool_id}/{interval}/{start}/{end}",
    response_model=List[PoolSeriesTableType],
)
async def get_pools_series(
    response: Response,
    session: AsyncSession = Depends(get_session),
    pool_id: int = None,
    interval: str = None,
    start: int = None,
    end: int = None,
) -> Union[List[PoolSeriesTableType], Response]:
    """
    Return list of pools price/volumes time series. To get the most up to data, use 0
     for the `end` parameter.
    """

    if interval not in INTERVALS:
        raise HTTPException(
            status_code=400,
            detail=f"Interval must be one of {', '.join([i for i in INTERVALS])}.",
        )

    num_records = (end - start) / INTERVAL_MAP[interval]["seconds"]
    if num_records > settings.MAX_TS_RECORDS:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum of {settings.MAX_TS_RECORDS} returned. Attempting to get "
            f"{num_records}...",
        )

    table = get_pool_series_table(table_suffix=INTERVAL_MAP[interval]["table_name"])

    query = select(table).where(
        table.chain_id == settings.CHAIN_ID,
        table.timestamp >= start,
        table.pool_id == pool_id,
    )

    if end != 0:
        query = query.where(table.timestamp <= end)

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


@router.get(
    "/pools/series/implied/{token_a}/{token_b}/{interval}/{start}/{end}",
    response_model=List[PoolSeriesTableType],
)
async def get_pools_series_implied(
    response: Response,
    token_a: str,
    token_b: str,
    interval: str,
    start: int,
    end: int,
    session: AsyncSession = Depends(get_session),
) -> Union[List[PoolSeriesTableType], Response]:
    """
    Return list of implied pool price/volumes time series, implied meaning there may not
     actually be a pool connecting the two tokens but we infer the price. To get the
     most up to data, use 0 for the `end` parameter.
    """
    if interval not in INTERVALS:
        raise HTTPException(
            status_code=400,
            detail=f"Interval must be one of {', '.join([i for i in INTERVALS])}.",
        )

    num_records = (end - start) / INTERVAL_MAP[interval]["seconds"]
    if num_records > settings.MAX_TS_RECORDS:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum of {settings.MAX_TS_RECORDS} returned. Attempting to get "
            f"{num_records}...",
        )
    table = get_token_series_table(table_suffix=INTERVAL_MAP[interval]["table_name"])

    # Since we are going from tokens to pools, we need to fill in data that is missing
    # in the tokens dimension, specifically the open / close. This is filled in by
    # subtracting the interval from the start time so that we get an additional data
    # point which is used for calculating the open for the requested start. We'll check
    # later if we are at beginning of series
    adjusted_start = start - INTERVAL_MAP[interval]["seconds"]

    token_a_query = (
        select(table)
        .where(
            table.chain_id == settings.CHAIN_ID,
            table.timestamp >= adjusted_start,
            table.address == token_a,
        )
        .order_by(table.timestamp.asc())
    )

    if end != 0:
        token_a_query = token_a_query.where(table.timestamp <= end)

    token_b_query = (
        select(table)
        .where(
            table.chain_id == settings.CHAIN_ID,
            table.timestamp >= adjusted_start,
            table.address == token_b,
        )
        .order_by(table.timestamp.asc())
    )

    if end != 0:
        token_b_query = token_b_query.where(table.timestamp <= end)

    result_token_a = await session.execute(token_a_query)
    result_token_b = await session.execute(token_b_query)

    timeseries_a: list[table] = result_token_a.scalars().all()
    timeseries_b: list[table] = result_token_b.scalars().all()

    min_time_series_len = min(len(timeseries_a), len(timeseries_b))
    # Check if exists
    if min_time_series_len == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)  # noqa

    def divide_attr(index, attr) -> float:
        return getattr(timeseries_a[index], attr) / getattr(timeseries_b[index], attr)

    output = []
    for i in range(min_time_series_len-1, 0, -1):

        if i < 3:
            pass

        output.append(PoolSeriesBase(
            chain_id=timeseries_a[i].chain_id,
            pool_id=-1,
            timestamp=timeseries_a[i].timestamp,
            close=divide_attr(i, "price"),
            open=divide_attr(i-1, "price"),
            high=divide_attr(i, "price_low"),
            low=divide_attr(i, "price_low"),
            base_volume=0,
            quote_volume=0,
            block_height=timeseries_a[i].block_height,
            total_supply=0,
            quote_lp_fees=0,
            quote_baln_fees=0,
            base_lp_fees=0,
            base_baln_fees=0,
        ))

    # Return the count in header
    total_count = str(len(output))
    response.headers["x-total-count"] = total_count

    return output


@router.get("/pools/dividends", response_model=List[Dividend])
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
