from datetime import datetime
from typing import Optional
import sqlalchemy as sa
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class DailyHistorical(SQLModel, table=True):
    timestamp: int = Field(primary_key=True, index=True)
    date: datetime = Field(None, sa_column=sa.Column(sa.DateTime(timezone=True)))
    update_interval: int = Field(None, index=False)
    days_since_launch: int = Field(None, index=True)

    address: Optional[str] = Field(primary_key=True, index=True)

    contract_name: Optional[str] = Field(primary_key=True, index=True)
    method: Optional[str] = Field(primary_key=True, index=True)
    value: Optional[float] = Field(None, index=False)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "daily_historicals"
