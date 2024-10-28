from __future__ import annotations

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from sqlmodel.main import SQLModelConfig


class Transaction(SQLModel, table=True):

    hash: str = Field(primary_key=True, index=True)

    timestamp: int | None = Field(None)
    transaction_index: int | None = Field(None)
    from_address: str | None = Field(None)
    to_address: str | None = Field(None)
    value: float | None = Field(None)
    status: str | None = Field(None)
    step_price: int | None = Field(None)
    step_used: int | None = Field(None)
    cumulative_step_used: int | None = Field(None)
    data: dict = Field(None)
    data_type: str | None = Field(None)
    score_address: str | None = Field(None)
    signature: str | None = Field(None)
    version: str | None = Field(None)
    method: str | None = Field(None)

    model_config = SQLModelConfig(
        extra="ignore",
    )

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "transactions"
