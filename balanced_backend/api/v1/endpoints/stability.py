from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession

from balanced_backend.db import get_session

router = APIRouter()


@router.get("/historical/stability")
async def contract_methods(
        response: Response,
        session: AsyncSession = Depends(get_session),
        skip: int = Query(0),
        limit: int = Query(1000, gt=0, lt=1001),
        start_timestamp: int = None,
        end_timestamp: int = None,
) -> Union[List, Response]:
    """Return list of stability fund balance over time."""
    query = "SELECT * FROM stability_fund_balance"
    conditions = []

    if start_timestamp is not None:
        conditions.append(f"timestamp >= {start_timestamp}")
    if end_timestamp is not None:
        conditions.append(f"timestamp <= {end_timestamp}")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += f" ORDER BY timestamp DESC LIMIT {limit} OFFSET {skip}"

    result = await session.execute(query)
    time_series = result.fetchall()

    # Check if exists
    if len(time_series) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    total_count = str(len(time_series))
    response.headers["x-total-count"] = total_count

    return time_series
