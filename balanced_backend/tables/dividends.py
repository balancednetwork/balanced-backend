from __future__ import annotations

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from sqlmodel.main import SQLModelConfig


class Dividend(SQLModel, table=True):

    chain_id: int | None = Field(None, primary_key=True)
    pool_id: int | None = Field(None, primary_key=True)
    base_address: str | None = Field(None, index=True)
    quote_address: str | None = Field(None, index=True)

    base_lp_fees_24h: float | None = Field(None)
    quote_lp_fees_24h: float | None = Field(None)
    base_baln_fees_24h: float | None = Field(None)
    quote_baln_fees_24h: float | None = Field(None)
    base_volume_24h: float | None = Field(None)
    quote_volume_24h: float | None = Field(None)

    base_lp_fees_30d: float | None = Field(None)
    quote_lp_fees_30d: float | None = Field(None)
    base_baln_fees_30d: float | None = Field(None)
    quote_baln_fees_30d: float | None = Field(None)
    base_volume_30d: float | None = Field(None)
    quote_volume_30d: float | None = Field(None)

    model_config = SQLModelConfig(
        extra="ignore",
    )

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "dividends"
