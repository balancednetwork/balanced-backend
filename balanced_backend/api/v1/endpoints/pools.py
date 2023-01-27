from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from balanced_backend.db import get_session
from balanced_backend.tables.pools import Pool

router = APIRouter()


@router.get("/pools")
async def pools(
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
            status_code=400,
            detail="Can only specify `pool_id` or `name`, not both."
        )

    if (pool_id or name) and \
            (quote_address or quote_symbol or base_address or quote_address):
        raise HTTPException(
            status_code=400,
            detail="Doesn't make sense to specify `pool_id` or `name`, with additional "
                   "parameters. Check your query."
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
        if type not in ['community', 'balanced']:
            raise HTTPException(
                status_code=400,
                detail="Parameter `type` must be one of 'community' or 'balanced'"
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
