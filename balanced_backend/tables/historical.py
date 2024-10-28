from __future__ import annotations

from datetime import datetime
from typing import Optional
import sqlalchemy as sa
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from sqlmodel.main import SQLModelConfig


class DailyHistorical(SQLModel, table=True):
    timestamp: int | None = Field(..., primary_key=True, index=True)
    date: datetime | None = Field(None, sa_column=sa.Column(sa.DateTime(timezone=True)))
    update_interval: int | None = Field(None, index=False)
    days_since_launch: int | None = Field(None, index=True)

    address: str | None = Field(..., primary_key=True, index=True)

    contract_name: str | None = Field(..., primary_key=True, index=True)
    method: str | None = Field(..., primary_key=True, index=True)
    value: float | None = Field(None, index=False)

    model_config = SQLModelConfig(
        extra="ignore",
    )

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "daily_historicals"
