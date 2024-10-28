from __future__ import annotations

from typing import Optional
from sqlalchemy.orm import declared_attr
from sqlalchemy.sql.schema import Column
from sqlmodel import Field, SQLModel, JSON
from sqlmodel.main import SQLModelConfig


class Token(SQLModel, table=True):
    address: str = Field(primary_key=True, index=True)
    chain_id: int = Field(primary_key=True, index=True)
    name: str | None = Field(None, index=True)
    symbol: str | None = Field(None, index=True)
    decimals: int | None = Field(None, index=False)
    logo_uri: str | None = Field(None, index=False)

    type: str | None = Field(None, index=False)
    is_stable: bool | None = Field(None, index=False)
    in_stability_fund: bool | None = Field(None, index=False)

    price: float | None = Field(None, index=False)
    price_24h: float | None = Field(None, index=False)
    price_7d: float | None = Field(None, index=False)
    price_30d: float | None = Field(None, index=False)

    path: dict | None = Field(None, sa_column=Column(JSON))
    pools: dict | None = Field(None, sa_column=Column(JSON))

    holders: int | None = Field(None, index=False)
    total_supply: float | None = Field(None, index=False)
    liquidity: float | None = Field(None)

    model_config = SQLModelConfig(
        extra="ignore",
    )

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "tokens"
