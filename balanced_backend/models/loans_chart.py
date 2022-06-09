from datetime import datetime
from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from pydantic import validator


class LoansChart(SQLModel, table=True):
    timestamp: Optional[int] = Field(default=None, primary_key=True)
    datetime: datetime = None
    value: Optional[float] = None

    @validator('datetime')
    def update_datetime_field(cls, v, values):
        if v is None:
            return datetime.fromtimestamp(values['timestamp'])
        return v

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "loans_chart"
