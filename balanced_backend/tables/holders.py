from __future__ import annotations

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from sqlmodel.main import SQLModelConfig


class Holder(SQLModel, table=True):
    address: str | None = Field(primary_key=True, index=True)
    pool_name: str | None = Field(None, index=True)
    pool_id: str | None = Field(None, index=True)
    base_address: str | None = Field(None, index=True)
    quote_address: str | None = Field(None, index=True)
    base_symbol: str | None = Field(None, index=True)
    quote_symbol: str | None = Field(None, index=True)
    quote_balance: str | None = Field(None, index=True)
    base_balance: str | None = Field(None, index=True)

    model_config = SQLModelConfig(
        extra="ignore",
    )

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "holders"
