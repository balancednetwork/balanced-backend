from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func

from balanced_backend.config import settings
from balanced_backend.db import get_session
from balanced_backend.tables.dex import DexSwap

router = APIRouter()


@router.get("/dex/swaps", response_model=list[DexSwap])
async def swaps(
        response: Response,
        session: AsyncSession = Depends(get_session),
        skip: int = Query(0),
        limit: int = Query(100, gt=0, lt=101),
        chain_id: int = Query(None),
        transaction_hash: str = Query(None),
        log_index: int = Query(None),
        start_timestamp: int = Query(None),
        end_timestamp: int = Query(None),
        start_block_number: int = Query(None),
        end_block_number: int = Query(None),

) -> list[DexSwap]:
    query = select(DexSwap).offset(skip).limit(limit).where(
        DexSwap.chain_id == settings.CHAIN_ID)
    query_count = select([func.count(DexSwap.chain_id)]).where(
        DexSwap.chain_id == settings.CHAIN_ID)

    if transaction_hash:
        query = query.where(DexSwap.transaction_hash == transaction_hash)
        query_count = query_count.where(DexSwap.transaction_hash == transaction_hash)
    if log_index:
        query = query.where(DexSwap.log_index == log_index)
        query_count = query.where(DexSwap.log_index == log_index)
    if chain_id:
        query = query.where(DexSwap.chain_id == chain_id)
        query_count = query.where(DexSwap.chain_id == chain_id)
    if start_timestamp:
        query = query.where(DexSwap.timestamp >= start_timestamp)
        query_count = query.where(DexSwap.timestamp >= start_timestamp)
    if end_timestamp:
        query = query.where(DexSwap.timestamp <= end_timestamp)
        query_count = query.where(DexSwap.timestamp <= end_timestamp)
    if start_block_number:
        query = query.where(DexSwap.block_number >= start_block_number)
        query_count = query.where(DexSwap.block_number >= start_block_number)
    if end_block_number:
        query = query.where(DexSwap.block_number <= end_block_number)
        query_count = query.where(DexSwap.block_number <= end_block_number)

    result = await session.execute(query)
    swaps = result.scalars().all()

    # # Return the count in header
    # # TODO: Can't be cached and very expensive... 2M records
    # result_count = await session.execute(query_count)
    # total_count = str(result_count.scalars().all()[0])
    # response.headers["x-total-count"] = total_count

    response.headers["x-total-count"] = str(len(swaps))
    return swaps
