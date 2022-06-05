from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, Query, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import func, select

from balanced_backend.db import get_session
from balanced_backend.models.loans_chart import LoansChart

router = APIRouter()


@router.get("/loans-chart")
async def get_delegations(
    response: Response,
    start_timestamp: int = -1,
    end_timestamp: int = -1,
    time_interval: int = -1,
    session: AsyncSession = Depends(get_session),
) -> Union[List[LoansChart], Response]:
    """Return list of delegations."""

    if start_timestamp == -1:
        raise HTTPException(status_code=400, detail="start_timestamp parameter is required")
    if end_timestamp == -1:
        raise HTTPException(status_code=400, detail="end_timestamp parameter is required")
    if time_interval == -1:
        raise HTTPException(status_code=400, detail="time_interval parameter is required")

    query = (
        select(LoansChart)
        .where(LoansChart.timestamp >= start_timestamp)
        .where(LoansChart.timestamp <= end_timestamp)
        .order_by(LoansChart.timestamp.desc())
    )

    result = await session.execute(query)
    loans_time_series = result.scalars().all()

    # Check if exists
    if len(loans_time_series) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    # # Return the count in header
    # query_count = select([func.count(LoansChart.address)]).where(LoansChart.address == address)
    # result_count = await session.execute(query_count)
    # total_count = str(result_count.scalars().all()[0])
    # response.headers["x-total-count"] = total_count

    return loans_time_series
