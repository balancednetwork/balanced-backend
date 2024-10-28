from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from sqlmodel.main import SQLModelConfig


class DexSwap(SQLModel, table=True):
    chain_id: int | None = Field(None, primary_key=True)
    transaction_hash: str = Field(None, primary_key=True)
    log_index: int | None = Field(None, primary_key=True)
    timestamp: int | None = Field(None, index=True)
    block_number: int | None = Field(None, index=True)
    pool_id: int | None | None = Field(None, index=True)

    from_token: str | None = Field(None)
    to_token: str | None = Field(None)

    base_token: str | None = Field(None)
    base_token_value: str | None = Field(None)
    base_token_value_decimal: float | None = Field(None)

    quote_token: str | None = Field(None)
    quote_token_value: str | None = Field(None)
    quote_token_value_decimal: float | None = Field(None)

    sender: str | None = Field(None)
    receiver: str | None = Field(None)
    from_value: str | None = Field(None)
    to_value: str | None = Field(None)
    lp_fees: str | None = Field(None)
    baln_fees: str | None = Field(None)
    pool_base: str | None = Field(None)
    pool_quote: str | None = Field(None)
    ending_price: str | None = Field(None)
    effective_fill_price: str | None = Field(None)

    from_value_decimal: float | None = Field(None)
    to_value_decimal: float | None = Field(None)
    lp_fees_decimal: float | None = Field(None)
    baln_fees_decimal: float | None = Field(None)
    pool_base_decimal: float | None = Field(None)
    pool_quote_decimal: float | None = Field(None)
    ending_price_decimal: float | None = Field(None)
    effective_fill_price_decimal: float | None = Field(None)

    model_config = SQLModelConfig(
        extra="ignore",
    )

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "dex_swaps"


class DexAdd(SQLModel, table=True):
    chain_id: int | None = Field(None, primary_key=True)
    transaction_hash: str | None = Field(None, primary_key=True)
    log_index: int | None = Field(None, primary_key=True)
    timestamp: int | None = Field(None, index=True)
    block_number: int | None = Field(None, index=True)

    pool_id: int | None = Field(None)
    owner: str | None = Field(None)
    value: str | None = Field(None)
    value_decimal: float | None = Field(None)
    base: str | None = Field(None)
    base_decimal: float | None = Field(None)
    quote: str | None = Field(None)
    quote_decimal: float | None = Field(None)

    model_config = SQLModelConfig(
        extra="ignore",
    )

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "dex_adds"
