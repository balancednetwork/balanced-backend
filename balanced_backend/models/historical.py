from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from pydantic import validator


class DailyHistorical(SQLModel, table=True):
    timestamp: Optional[int] = Field(primary_key=True)
    date: datetime = Field(None, sa_column=sa.Column(sa.DateTime(timezone=True)))
    update_interval: int = Field(None, index=True)
    days_since_launch: int = Field(None, index=True)

    address: Optional[str] = Field(primary_key=True)

    contract_name: Optional[str] = Field(None, index=True)
    method: Optional[str] = Field(primary_key=True)
    value: Optional[float] = None

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "daily_historical"
