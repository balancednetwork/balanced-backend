from typing import TYPE_CHECKING
from http import HTTPStatus
from typing import List, Union
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from balanced_backend.db import get_session
from balanced_backend.tables.tokens import Token
from balanced_backend.api.v1.endpoints.pools import INTERVALS, INTERVAL_MAP
from balanced_backend.config import settings
from balanced_backend.tables.utils import get_token_series_table

if TYPE_CHECKING:
    from balanced_backend.tables.utils import TokenSeriesTableType

router = APIRouter()


@router.get("/tokens")
async def tokens(
        response: Response,
        session: AsyncSession = Depends(get_session),
        address: str = None,
        name: str = None,
        symbol: str = None,
        type: str = None,
) -> Union[List[Token], Response]:
    """Return list of delegations."""

    query = select(Token)

    if address is not None:
        query = query.where(Token.address == address)
    elif name is not None:
        query = query.where(Token.name == name)
    elif symbol is not None:
        query = query.where(Token.symbol == symbol)
    elif type is not None:
        if type not in ['community', 'balanced']:
            raise HTTPException(
                status_code=400,
                detail="Parameter `type` must be one of 'community' or 'balanced'"
            )
        query = query.where(Token.type == type)

    result = await session.execute(query)
    tokens = result.scalars().all()

    # Check if exists
    if len(tokens) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    # Return the count in header
    total_count = str(len(tokens))
    response.headers["x-total-count"] = total_count

    return tokens


@router.get("/tokens/series/{interval}/{start}/{end}")
async def get_pools_series(
        response: Response,
        session: AsyncSession = Depends(get_session),
        interval: str = None,
        start: int = None,
        end: int = None,
        address: str = None,
        symbol: str = None,
) -> Union[List['TokenSeriesTableType'], Response]:
    """Return list of pools price/volumes time series."""
    if address is None and symbol is None:
        raise HTTPException(
            status_code=400,
            detail=f"Must supply either a token address or symbol as query parameter."
        )

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

    table = get_token_series_table(table_suffix=INTERVAL_MAP[interval]['table_name'])

    query = select(table).where(
        table.chain_id == settings.CHAIN_ID,
        table.timestamp >= start,
        table.timestamp <= end,
    )

    if address is not None:
        query = query.where(table.address == address)
    if symbol is not None:
        query = query.where(table.symbol == symbol)

    query = query.order_by(table.timestamp.desc())

    result = await session.execute(query)
    timeseries: list[table] = result.scalars().all()

    # Check if exists
    if len(timeseries) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)  # noqa

    # Return the count in header
    total_count = str(len(timeseries))
    response.headers["x-total-count"] = total_count

    return timeseries
