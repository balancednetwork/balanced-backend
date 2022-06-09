from datetime import datetime
from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class BnusdSupplyChart(SQLModel, table=True):
    timestamp: Optional[int] = Field(default=None, primary_key=True)
    datetime: datetime
    value: Optional[float]

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "bnusd_supply_chart"
