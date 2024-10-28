from datetime import datetime

from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, Response, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func

from balanced_backend.db import get_session
from balanced_backend.tables.holders import Holder

router = APIRouter()


@router.get("/holders", response_model=list[Holder])
async def holders(
        response: Response,
        session: AsyncSession = Depends(get_session),
        skip: int = Query(0),
        limit: int = Query(100, gt=0, lt=101),
        address: str = Query(None),
        pool_name: str = Query(None),
        pool_id: str = Query(None),
        base_address: str = Query(None),
        quote_address: str = Query(None),
        base_symbol: str = Query(None),
        quote_symbol: str = Query(None),
        quote_balance: str = Query(None),
        base_balance: str = Query(None),
) -> Union[List[Holder], Response]:
    """Return list of delegations."""

    query = select(Holder).offset(skip).limit(limit)
    query_count = select([func.count(Holder.address)])

    if pool_id and pool_name:
        raise HTTPException(
            status_code=400,
            detail="Can only specify `pool_id` or `pool_name`, not both."
        )

    if quote_balance is not None:
        if quote_balance[0] == '+':
            quote_greater_than: bool = True
            quote_balance = quote_balance[:-1]
        elif quote_balance[0] == '+':
            quote_greater_than: bool = True
            quote_balance = quote_balance[:-1]
        else:
            quote_greater_than: bool = True

    if base_balance is not None:
        if base_balance[0] == '+':
            base_greater_than: bool = True
            base_balance = base_balance[:-1]
        elif base_balance[0] == '+':
            base_greater_than: bool = True
            base_balance = base_balance[:-1]
        else:
            base_greater_than: bool = True


    if pool_id is not None:
        query = query.where(Holder.pool_id == pool_id)
        query_count = query_count.where(Holder.pool_id == pool_id)
    elif pool_name is not None:
        query = query.where(Holder.pool_name == pool_name)
        query_count = query_count.where(Holder.pool_name == pool_name)

    if address is not None:
        query = query.where(Holder.address == address)
        query_count = query_count.where(Holder.address == address)
    if base_address is not None:
        query = query.where(Holder.base_address == base_address)
        query_count = query_count.where(Holder.base_address == base_address)
    if quote_address is not None:
        query = query.where(Holder.quote_address == quote_address)
        query_count = query_count.where(Holder.quote_address == quote_address)
    if base_symbol is not None:
        query = query.where(Holder.base_symbol == base_symbol)
        query_count = query_count.where(Holder.base_symbol == base_symbol)
    if quote_symbol is not None:
        query = query.where(Holder.quote_symbol == quote_symbol)
        query_count = query_count.where(Holder.quote_symbol == quote_symbol)

    result_count = await session.execute(query_count)
    result = await session.execute(query)

    total_count = str(result_count.scalars().all()[0])
    holders = result.scalars().all()

    # Return the count in header
    response.headers["x-total-count"] = total_count

    return holders
