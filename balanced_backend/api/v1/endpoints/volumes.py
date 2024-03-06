from datetime import datetime

from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, Response, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from balanced_backend.db import get_session
from balanced_backend.tables.volumes import ContractMethodVolume

router = APIRouter()


@router.get("/contract-volumes")
async def contract_volumes(
        session: AsyncSession = Depends(get_session),
        skip: int = Query(0),
        limit: int = Query(1000, gt=0, lt=1001),
        address: str = None,
        contract_name: str = None,
        method: str = None,
        days_ago: int = None,
        start_timestamp: int = None,
        end_timestamp: int = None,
        start_date: datetime = None,
        end_date: datetime = None,
) -> Union[List[ContractMethodVolume], Response]:
    """Return list of delegations."""

    query = select(ContractMethodVolume).offset(skip).limit(limit).order_by(
        ContractMethodVolume.end_timestamp.desc()
    )

    if address is not None:
        query = query.where(ContractMethodVolume.address == address)
    elif contract_name is not None:
        query = query.where(ContractMethodVolume.contract_name == contract_name)
    else:
        raise HTTPException(
            status_code=400,
            detail="Either address or contract_name must be supplied"
        )

    if method is not None:
        query = query.where(ContractMethodVolume.method == method)

    if start_date is not None:
        query = query.where(ContractMethodVolume.start_date >= start_date)

        if end_date is not None:
            query = query.where(ContractMethodVolume.end_date <= end_date)

    elif days_ago is not None:
        end_timestamp = datetime.utcnow().timestamp()
        start_timestamp = datetime.utcnow().timestamp() - \
                          (24 * 60 * 60) * days_ago
        query = query \
            .where(ContractMethodVolume.start_timestamp >= start_timestamp) \
            .where(ContractMethodVolume.end_timestamp <= end_timestamp)

    elif start_timestamp is not None:
        query = query.where(ContractMethodVolume.start_timestamp <= start_timestamp)

    elif end_timestamp is not None:
        query = query.where(ContractMethodVolume.end_timestamp >= end_timestamp)

    result = await session.execute(query)
    time_series = result.scalars().all()

    # Check if exists
    if len(time_series) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    # # Return the count in header
    # query_count = select([func.count(LoansChart.address)]).where(LoansChart.address == address)
    # result_count = await session.execute(query_count)
    # total_count = str(result_count.scalars().all()[0])
    # response.headers["x-total-count"] = total_count

    return time_series

# TODO: RM after FE change
@router.get("/contract-method-volumes")
async def contract_volumes(
        session: AsyncSession = Depends(get_session),
        skip: int = Query(0),
        limit: int = Query(1000, gt=0, lt=1001),
        address: str = None,
        contract_name: str = None,
        method: str = None,
        days_ago: int = None,
        start_timestamp: int = None,
        end_timestamp: int = None,
        start_date: datetime = None,
        end_date: datetime = None,
) -> Union[List[ContractMethodVolume], Response]:
    """Return list of delegations."""

    query = select(ContractMethodVolume).offset(skip).limit(limit).order_by(
        ContractMethodVolume.end_timestamp.desc()
    )

    if address is not None:
        query = query.where(ContractMethodVolume.address == address)
    elif contract_name is not None:
        query = query.where(ContractMethodVolume.contract_name == contract_name)
    else:
        raise HTTPException(
            status_code=400,
            detail="Either address or contract_name must be supplied"
        )

    if method is not None:
        query = query.where(ContractMethodVolume.method == method)

    if start_date is not None:
        query = query.where(ContractMethodVolume.start_date >= start_date)

        if end_date is not None:
            query = query.where(ContractMethodVolume.end_date <= end_date)

    elif days_ago is not None:
        end_timestamp = datetime.utcnow().timestamp()
        start_timestamp = datetime.utcnow().timestamp() - \
                          (24 * 60 * 60) * days_ago
        query = query \
            .where(ContractMethodVolume.start_timestamp >= start_timestamp) \
            .where(ContractMethodVolume.end_timestamp <= end_timestamp)

    elif start_timestamp is not None:
        query = query.where(ContractMethodVolume.start_timestamp <= start_timestamp)

    elif end_timestamp is not None:
        query = query.where(ContractMethodVolume.end_timestamp >= end_timestamp)

    result = await session.execute(query)
    time_series = result.scalars().all()

    # Check if exists
    if len(time_series) == 0:
        return Response(status_code=HTTPStatus.NO_CONTENT.value)

    # # Return the count in header
    # query_count = select([func.count(LoansChart.address)]).where(LoansChart.address == address)
    # result_count = await session.execute(query_count)
    # total_count = str(result_count.scalars().all()[0])
    # response.headers["x-total-count"] = total_count

    return time_series