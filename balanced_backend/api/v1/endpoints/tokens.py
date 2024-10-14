from typing import TYPE_CHECKING, Optional
from http import HTTPStatus
from typing import List, Union
from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.exc import NoResultFound, DBAPIError
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
    """Return list of tokens."""

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


async def get_token_series_interval(
        response: Response,
        session: AsyncSession = Depends(get_session),
        interval: str = None,
        start: int = None,
        end: int = None,
        address: str = None,
        symbol: str = None,
):
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
    )

    # If end is not 0, add it to the query
    if end != 0:
        query = query.where(table.timestamp <= end)

    if address is not None:
        query = query.where(table.address == address)
    if symbol is not None:
        query = query.where(table.symbol == symbol)

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


@router.get("/tokens/series/{interval}/{start}/{end}")
async def get_tokens_series(
        response: Response,
        session: AsyncSession = Depends(get_session),
        interval: str = None,
        start: int = None,
        end: int = None,
        address: str = None,
        symbol: str = None,
) -> Union[List['TokenSeriesTableType'], Response]:
    """
    Return list of tokens price/volumes time series. Either symbol or address must be
     supplied. To get the most up to date data, use 0 for the `end` parameter.
    """
    return await get_token_series_interval(
        response=response,
        session=session,
        interval=interval,
        start=start,
        end=end,
        address=address,
        symbol=symbol,
    )


async def get_token_price_latest(
        *,
        table: 'TokenSeriesTableType',
        session: AsyncSession,
        response: Response,
        address: str = None,
        symbol: str = None,
) -> Union[List['TokenSeriesTableType'], Response]:
    # This happens when the block height / timestamp is above the last record
    query = select(table).where(
        table.chain_id == settings.CHAIN_ID,
    ).order_by(table.timestamp.desc()).limit(1)

    if address is not None:
        query = query.where(
            table.address == address
        )
    else:
        query = query.where(
            table.symbol == symbol
        )

    result = await session.execute(query)

    prices = result.scalars().all()
    if len(prices) == 0:
        raise HTTPException(
            status_code=204,
            detail=f"No result found with that symbol / address"
        )

    # Return the count in header
    response.headers["x-total-count"] = "1"

    return [prices[0]]


async def get_token_price(
        *,
        interval: str,
        response: Response,
        session: AsyncSession,
        height: int,
        timestamp: int,
        address: str,
        symbol: str,
        head: bool,
) -> Union[List['TokenSeriesTableType'], Response]:
    if address is None and symbol is None:
        raise HTTPException(
            status_code=400,
            detail=f"Must supply either a token address or symbol as query parameter."
        )
    if height is not None and timestamp is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Can't supply both height and timestamp as query param."
        )

    table = get_token_series_table(table_suffix=INTERVAL_MAP[interval]['table_name'])

    if head:
        return await get_token_price_latest(
            table=table,
            session=session,
            response=response,
            address=address,
            symbol=symbol,
        )

    query = select(table).where(
        table.chain_id == settings.CHAIN_ID,
    ).limit(1)

    if address is not None:
        query = query.where(
            table.address == address
        )
    elif symbol is not None:
        query = query.where(
            table.symbol == symbol
        )
    else:
        raise Exception("Should never happen.")

    if timestamp is not None:
        query = query.where(
            table.timestamp <= timestamp,
        ).order_by(
            table.timestamp.desc()
        )
    elif height is not None:
        query = query.where(
            table.block_height <= height,
        ).order_by(
            table.block_height.desc()
        )
    else:
        raise Exception("Should never happen")

    try:
        result = await session.execute(query)
    except DBAPIError as e:
        raise HTTPException(
            status_code=400,
            detail=f"One of your parameters is out of scale"
        )

    try:
        prices = result.scalars().all()
        if len(prices) == 0:
            raise HTTPException(
                status_code=204,
                detail=f"No result found..."
            )
    except NoResultFound:
        return await get_token_price_latest(
            table=table,
            session=session,
            response=response,
            address=address,
            symbol=symbol,
        )

    # Return the count in header
    response.headers["x-total-count"] = "1"

    return [prices[0]]


@router.get("/tokens/prices")
async def get_tokens_prices(
        response: Response,
        session: AsyncSession = Depends(get_session),
        height: int = None,
        timestamp: int = None,
        interval: str = None,
        start: int = None,
        end: int = None,
        address: str = None,
        symbol: str = None,
        head: bool = False,
) -> Union[List['TokenSeriesTableType'], Response]:
    """
    Return list of token prices/volumes over an interval with `start`/`end` timestamps
    or the closest price when given the `height`/`timestamp` value.
    """
    if timestamp is not None and timestamp < 1619404096:
        raise HTTPException(
            status_code=400,
            detail=f"timestamp must be above 1619404096."
        )

    if height is not None and height < 33585760:
        raise HTTPException(
            status_code=400,
            detail=f"height must be above 33585760."
        )

    if start is not None or end is not None:
        return await get_token_series_interval(
            response=response,
            session=session,
            interval=interval,
            start=start,
            end=end,
            address=address,
            symbol=symbol,
        )
    elif height is not None or timestamp is not None:
        if interval is None:
            interval = '5m'

        return await get_token_price(
            interval=interval,
            response=response,
            session=session,
            height=height,
            timestamp=timestamp,
            address=address,
            symbol=symbol,
            head=head,
        )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Must supply either a start/end or height/timestamp as query "
                   f"parameters."
        )
