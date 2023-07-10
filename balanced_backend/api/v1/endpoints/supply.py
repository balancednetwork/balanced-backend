from http import HTTPStatus
from typing import Union
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from balanced_backend.db import get_session
from balanced_backend.tables.tokens import Token
from balanced_backend.config import settings

router = APIRouter()


@router.get("/token/circulating-supply/symbol/{symbol}")
async def get_coingecko_summary(
        session: AsyncSession = Depends(get_session),
        symbol: str = None,
) -> Union[float, Response]:
    query = select(
        Token.total_supply
    ).where(
        Token.symbol == symbol,
        Token.chain_id == settings.CHAIN_ID,
    )

    result = await session.execute(query)
    total_supply = result.scalars().all()
    if len(total_supply) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    return total_supply[0]


@router.get("/token/circulating-supply/address/{address}")
async def get_coingecko_summary(
        session: AsyncSession = Depends(get_session),
        address: str = None,
) -> Union[float, Response]:
    query = select(
        Token.total_supply
    ).where(
        Token.address == address,
        Token.chain_id == settings.CHAIN_ID,
    )

    result = await session.execute(query)
    total_supply = result.scalars().all()
    if len(total_supply) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    return total_supply[0]
