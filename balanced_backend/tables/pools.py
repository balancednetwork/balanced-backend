from __future__ import annotations

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from sqlmodel.main import SQLModelConfig


class Pool(SQLModel, table=True):
    base_address: str = Field(primary_key=True, index=True)
    quote_address: str = Field(primary_key=True, index=True)

    chain_id: int | None = Field(None, index=True)
    pool_id: int | None = Field(None, index=True)
    name: str | None = Field(None, index=True)
    base_name: str | None = Field(None, index=True)
    quote_name: str | None = Field(None, index=True)
    base_symbol: str | None = Field(None, index=True)
    quote_symbol: str | None = Field(None, index=True)
    base_decimals: int | None = Field(None)
    quote_decimals: int | None = Field(None)

    type: str | None = Field(None, index=True)

    price: float | None = Field(None)
    price_24h: float | None = Field(None)
    price_7d: float | None = Field(None)
    price_30d: float | None = Field(None)

    price_change_24h: float | None = Field(None)
    price_change_7d: float | None = Field(None)
    price_change_30d: float | None = Field(None)

    price_24h_low: float | None = Field(None)
    price_24h_high: float | None = Field(None)

    base_volume_24h: float | None = Field(None)
    quote_volume_24h: float | None = Field(None)
    base_lp_fees_24h: float | None = Field(None)
    quote_lp_fees_24h: float | None = Field(None)
    base_baln_fees_24h: float | None = Field(None)
    quote_baln_fees_24h: float | None = Field(None)

    base_volume_30d: float | None = Field(None)
    quote_volume_30d: float | None = Field(None)
    base_lp_fees_30d: float | None = Field(None)
    quote_lp_fees_30d: float | None = Field(None)
    base_baln_fees_30d: float | None = Field(None)
    quote_baln_fees_30d: float | None = Field(None)

    base_price: float | None = Field(None)
    quote_price: float | None = Field(None)
    base_supply: float | None = Field(None)
    quote_supply: float | None = Field(None)
    base_liquidity: float | None = Field(None)
    quote_liquidity: float | None = Field(None)

    holders: int | None = Field(None)
    total_supply: float | None = Field(None)
    last_updated_timestamp: int | None = Field(None)

    model_config = SQLModelConfig(
        extra="ignore",
    )

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "pools"
