from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from sqlmodel.main import SQLModelConfig


class ContractMethodVolume(SQLModel, table=True):
    address: str = Field(primary_key=True)
    method: str = Field(primary_key=True)

    contract_name: str | None = Field(None, index=True)

    start_timestamp: int | None = Field(primary_key=True)
    end_timestamp: int | None = Field(primary_key=True)

    start_date: datetime = Field(
        None,
        sa_column=sa.Column(sa.DateTime(timezone=True), index=True))
    end_date: datetime = Field(
        None, sa_column=sa.Column(sa.DateTime(timezone=True), index=True))

    start_block: int
    end_block: int
    update_interval: int | None = Field(None, index=True)
    days_since_launch: int | None = Field(None, index=True)
    value: float
    num_events: int

    model_config = SQLModelConfig(
        extra="ignore",
    )

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "contract_method_volumes"
