from datetime import timedelta, datetime
from http import HTTPStatus
from typing import List, Union, Dict

from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession

from balanced_backend.db import get_session
from balanced_backend.utils.rpc import get_icx_call
from balanced_backend.log import logger

router = APIRouter()


@router.get("/historical/stability", response_model=List)
async def historical_stability(
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


stability_cached_output = None
stability_last_updated = None


@router.get("/stability/balances", response_model=Dict)
async def stability_token_balances() -> Union[Dict, Response]:
    global stability_cached_output, stability_last_updated

    now = datetime.now()

    if (
        stability_cached_output is not None
        and stability_last_updated is not None
        and now - stability_last_updated < timedelta(minutes=2)
    ):
        return stability_cached_output

    resp = get_icx_call(
        to_address="cxa09dbb60dcb62fffbd232b6eae132d730a2aafa6",
        params={"method": "getAcceptedTokens"},
    )

    if resp.status_code == 200:
        stability_tokens = resp.json()["result"]
    else:
        logger.info(f"Bad response get stability tokens - {resp.status_code}")
        if stability_cached_output is not None:
            return stability_cached_output
        return Response(status_code=HTTPStatus.NO_CONTENT.value)  # noqa

    stability_cached_output = {}
    for i in stability_tokens:
        resp = get_icx_call(
            to_address=i,
            params={
                "method": "balanceOf",
                "params": {"_owner": "cxa09dbb60dcb62fffbd232b6eae132d730a2aafa6"},
            },
        )
        if resp.status_code == 200:
            balance = int(resp.json()["result"], 0)
        else:
            logger.info(f"Bad response get stability balance - {resp.status_code}")
            if len(stability_cached_output) == len(stability_tokens):
                return stability_cached_output
            return Response(status_code=HTTPStatus.NO_CONTENT.value)  # noqa

        resp = get_icx_call(
            to_address=i,
            params={"method": "decimals"},
        )
        if resp.status_code == 200:
            decimals = int(resp.json()["result"], 0)
        else:
            logger.info(f"Bad response get stability decimals - {resp.status_code}")
            if len(stability_cached_output) == len(stability_tokens):
                return stability_cached_output
            return Response(status_code=HTTPStatus.NO_CONTENT.value)  # noqa

        stability_cached_output[i] = balance / 10**decimals

    stability_last_updated = datetime.now()
    return stability_cached_output
