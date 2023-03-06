from typing import Union
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from balanced_backend.db import get_session
from balanced_backend.tables.stats import Stats

router = APIRouter()


@router.get("/stats")
async def get_stats(
        session: AsyncSession = Depends(get_session),
) -> Union[Stats, Response]:
    """Return balanced stats."""
    query = select(Stats)
    result = await session.execute(query)

    return result.scalars().first()
