import datetime
from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from balanced_backend.db import get_session
from balanced_backend.models.historical import DailyHistorical

router = APIRouter()


@router.get("/historical")
async def historical_daily(
    address: str = None,
    contract_name: str = None,
    method: str = None,
    days_ago: int = None,
    start_timestamp: int = None,
    end_timestamp: int = None,
    session: AsyncSession = Depends(get_session),
) -> Union[List[DailyHistorical], Response]:
    """Return list of delegations."""

    query = select(DailyHistorical)

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
        start_timestamp = datetime.datetime.utcnow().timestamp()
        end_timestamp = datetime.datetime.utcnow().timestamp() - \
                        (24 * 60 * 60) * days_ago

        query = query\
            .where(DailyHistorical.timestamp >= start_timestamp)\
            .where(DailyHistorical.timestamp <= end_timestamp)

    elif start_timestamp is not None:
        query = query.where(DailyHistorical.timestamp >= start_timestamp)
    elif end_timestamp is not None:
        query = query.where(DailyHistorical.timestamp >= start_timestamp)

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
