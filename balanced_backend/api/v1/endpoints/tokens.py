from datetime import datetime

from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, Response, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from balanced_backend.db import get_session
from balanced_backend.tables.tokens import Token, TokenPrice, TokenPool

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


@router.get("/token/pools")
async def token_pool_prices(
        session: AsyncSession = Depends(get_session),
        skip: int = Query(0),
        limit: int = Query(1000, gt=0, lt=1001),
        address: str = None,
        symbol: str = None,
        reference_address: str = None,
        reference_symbol: str = None,
        pool_id: int = None,
        pool_name: int = None,
) -> Union[List[TokenPool], Response]:
    """Return list of all tokens in their pools."""

    query = select(TokenPool).offset(skip).limit(limit)

    if address is not None:
        query = query.where(TokenPool.address == address)
    if symbol is not None:
        query = query.where(TokenPool.symbol == symbol)
    if reference_address is not None:
        query = query.where(TokenPool.reference_address == reference_address)
    if reference_symbol is not None:
        query = query.where(TokenPool.reference_symbol == reference_symbol)
    if pool_id is not None:
        query = query.where(TokenPool.pool_id == pool_id)
    if pool_name is not None:
        query = query.where(TokenPool.pool_name == pool_name)


    result = await session.execute(query)
    time_series = result.scalars().all()

    # Check if exists
    if len(time_series) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    return time_series


# @router.get("/token/prices")
# async def token_prices(
#         session: AsyncSession = Depends(get_session),
#         skip: int = Query(0),
#         limit: int = Query(1000, gt=0, lt=1001),
#         address: str = None,
#         contract_name: str = None,
#         days_ago: int = None,
#         start_timestamp: int = None,
#         end_timestamp: int = None,
#         start_date: datetime = None,
#         end_date: datetime = None,
# ) -> Union[List[TokenPrice], Response]:
#     """Return list of token prices."""
#
#     query = select(TokenPrice).offset(skip).limit(limit)
#
#     if address is not None:
#         query = query.where(TokenPrice.address == address)
#     elif contract_name is not None:
#         query = query.where(TokenPrice.contract_name == contract_name)
#     else:
#         raise HTTPException(
#             status_code=400,
#             detail="Either address or contract_name must be supplied"
#         )
#
#     if start_date is not None:
#         query = query.where(TokenPrice.start_date >= start_date)
#
#         if end_date is not None:
#             query = query.where(TokenPrice.end_date <= end_date)
#
#     elif days_ago is not None:
#         end_timestamp = datetime.utcnow().timestamp()
#         start_timestamp = datetime.utcnow().timestamp() - \
#                           (24 * 60 * 60) * days_ago
#         query = query \
#             .where(TokenPrice.start_timestamp >= start_timestamp) \
#             .where(TokenPrice.end_timestamp <= end_timestamp)
#
#     elif start_timestamp is not None:
#         query = query.where(TokenPrice.start_timestamp <= start_timestamp)
#
#     elif end_timestamp is not None:
#         query = query.where(TokenPrice.end_timestamp >= end_timestamp)
#
#     result = await session.execute(query)
#     time_series = result.scalars().all()
#
#     # Check if exists
#     if len(time_series) == 0:
#         return Response(status_code=HTTPStatus.NO_CONTENT.value)
#
#     # # Return the count in header
#     # query_count = select([func.count(LoansChart.address)]).where(LoansChart.address == address)
#     # result_count = await session.execute(query_count)
#     # total_count = str(result_count.scalars().all()[0])
#     # response.headers["x-total-count"] = total_count
#
#     return time_series