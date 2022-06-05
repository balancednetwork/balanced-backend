from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class LoansChart(SQLModel, table=True):
    time: str = Field(primary_key=True)

    timestamp: Optional[int] = Field(None, index=False),

    value: Optional[float] = Field(None, index=False)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "loans_chart"
