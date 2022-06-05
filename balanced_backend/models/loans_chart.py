from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel, Column, BigInteger


class LoansChart(SQLModel, table=True):
    # timestamp: Optional[int] = Field(default_factory=next_val, sa_column=Column(BigInteger(), primary_key=True, autoincrement=False))
    timestamp: Optional[int] = Field(default=None, primary_key=True)

    value: Optional[float] = Field(None, index=False)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "loans_chart"
