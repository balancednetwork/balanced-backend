from __future__ import annotations

from typing import NewType, Union

from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel, Field
from sqlmodel.main import SQLModelConfig


class TokenSeriesBase(SQLModel):
    address: str = Field(primary_key=True)
    timestamp: int = Field(primary_key=True)
    chain_id: int | None = Field(None, index=True)
    symbol: str | None = Field(None, index=True)
    price: float | None = Field(None)
    price_high: float | None = Field(None)
    price_low: float | None = Field(None)
    block_height: int | None = Field(None)
    # The latest record which doesn't fall in normal interval. Can be only one.
    head: bool = Field(False)

    model_config = SQLModelConfig(
        extra="ignore",
    )


class TokenSeries5Min(TokenSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "token_series_5_min"


class TokenSeries15Min(TokenSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "token_series_15_min"


class TokenSeries1Hour(TokenSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "token_series_1_hour"


class TokenSeries4Hour(TokenSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "token_series_4_hour"


class TokenSeries1Day(TokenSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "token_series_1_day"


class TokenSeries1Week(TokenSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "token_series_1_week"


class TokenSeries1Month(TokenSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "token_series_1_month"


TokenSeriesTableType = NewType(
    'TableType',
    Union[
        TokenSeries5Min,
        TokenSeries15Min,
        TokenSeries1Hour,
        TokenSeries4Hour,
        TokenSeries1Day,
        TokenSeries1Month,
    ]
)


class PoolSeriesBase(SQLModel):
    chain_id: int | None = Field(None, primary_key=True)
    pool_id: int | None = Field(None, primary_key=True)
    timestamp: int | None = Field(None, primary_key=True)

    close: float | None = Field(None)
    open: float | None = Field(None)
    high: float | None = Field(None)
    low: float | None = Field(None)

    base_volume: float | None = Field(None)
    quote_volume: float | None = Field(None)
    block_height: int | None = Field(None)
    total_supply: float | None = Field(None)

    quote_lp_fees: float | None = Field(None)
    quote_baln_fees: float | None = Field(None)
    base_lp_fees: float | None = Field(None)
    base_baln_fees: float | None = Field(None)

    # The latest record which doesn't fall in normal interval. Can be only one.
    # head: bool = Field(False)

    model_config = SQLModelConfig(
        extra="ignore",
    )


class PoolSeries5Min(PoolSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "pool_series_5_min"


class PoolSeries15Min(PoolSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "pool_series_15_min"


class PoolSeries1Hour(PoolSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "pool_series_1_hour"


class PoolSeries4Hour(PoolSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "pool_series_4_hour"


class PoolSeries1Day(PoolSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "pool_series_1_day"


class PoolSeries1Week(PoolSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "pool_series_1_week"


class PoolSeries1Month(PoolSeriesBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "pool_series_1_month"


PoolSeriesTableType = NewType(
    'TableType',
    Union[
        PoolSeries5Min,
        PoolSeries15Min,
        PoolSeries1Hour,
        PoolSeries4Hour,
        PoolSeries1Day,
        PoolSeries1Month,
    ]
)
