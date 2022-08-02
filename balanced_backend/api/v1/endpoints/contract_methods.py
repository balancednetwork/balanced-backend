import datetime
from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, Response, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from balanced_backend.db import get_session
from balanced_backend.tables.historical import DailyHistorical

router = APIRouter()


@router.get("/contract-methods")
async def contract_methods(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0),
    limit: int = Query(1000, gt=0, lt=1001),
    address: str = None,
    contract_name: str = None,
    method: str = None,
    days_ago: int = None,
    start_timestamp: int = None,
    end_timestamp: int = None,
) -> Union[List[DailyHistorical], Response]:
    """Return list of contract methods over time."""

    query = select(DailyHistorical).offset(skip).limit(limit)

    if address is not None:
        query = query.where(DailyHistorical.address == address)
    elif contract_name is not None:
        query = query.where(DailyHistorical.contract_name == contract_name)
    else:
        raise HTTPException(
            status_code=400,
            detail="Either address or contract_name must be supplied"
        )

    if method is not None:
        query = query.where(DailyHistorical.method == method)

    if days_ago is not None:
        end_timestamp = datetime.datetime.utcnow().timestamp()
        start_timestamp = datetime.datetime.utcnow().timestamp() - \
                        (24 * 60 * 60) * days_ago

        query = query\
            .where(DailyHistorical.timestamp >= start_timestamp)\
            .where(DailyHistorical.timestamp <= end_timestamp)

    elif start_timestamp is not None:
        query = query.where(DailyHistorical.timestamp <= start_timestamp)
    elif end_timestamp is not None:
        query = query.where(DailyHistorical.timestamp >= end_timestamp)

    result = await session.execute(query)
    time_series = result.scalars().all()

    # Check if exists
    if len(time_series) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    # # Return the count in header
    # query_count = select([func.count(LoansChart.address)]).where(LoansChart.address == address)
    # result_count = await session.execute(query_count)
    # total_count = str(result_count.scalars().all()[0])
    # response.headers["x-total-count"] = total_count

    return time_series


# TODO: RM after FE change
@router.get("/historical")
async def historical(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0),
    limit: int = Query(1000, gt=0, lt=1001),
    address: str = None,
    contract_name: str = None,
    method: str = None,
    days_ago: int = None,
    start_timestamp: int = None,
    end_timestamp: int = None,
) -> Union[List[DailyHistorical], Response]:
    query = select(DailyHistorical).offset(skip).limit(limit)

    if address is not None:
        query = query.where(DailyHistorical.address == address)
    elif contract_name is not None:
        query = query.where(DailyHistorical.contract_name == contract_name)
    else:
        raise HTTPException(
            status_code=400,
            detail="Either address or contract_name must be supplied"
        )

    if method is not None:
        query = query.where(DailyHistorical.method == method)

    if days_ago is not None:
        end_timestamp = datetime.datetime.utcnow().timestamp()
        start_timestamp = datetime.datetime.utcnow().timestamp() - \
                        (24 * 60 * 60) * days_ago

        query = query\
            .where(DailyHistorical.timestamp >= start_timestamp)\
            .where(DailyHistorical.timestamp <= end_timestamp)

    elif start_timestamp is not None:
        query = query.where(DailyHistorical.timestamp <= start_timestamp)
    elif end_timestamp is not None:
        query = query.where(DailyHistorical.timestamp >= end_timestamp)

    result = await session.execute(query)
    time_series = result.scalars().all()

    # Check if exists
    if len(time_series) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    return time_series
