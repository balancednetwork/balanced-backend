from typing import Optional, NewType, Union

from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel, Field


class TokenSeriesBase(SQLModel):
    address: Optional[str] = Field(primary_key=True)
    timestamp: Optional[int] = Field(primary_key=True)
    chain_id: int = Field(None, index=True)
    symbol: str = Field(None, index=True)
    price: float = Field(None)
    price_high: float = Field(None)
    price_low: float = Field(None)
    block_height: int = Field(None)

    class Config:
        extra = "ignore"


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
    chain_id: int = Field(None, primary_key=True)
    pool_id: int = Field(None, primary_key=True)
    timestamp: int = Field(None, primary_key=True)

    close: float = Field(None)
    open: float = Field(None)
    high: float = Field(None)
    low: float = Field(None)

    base_volume: float = Field(None)
    quote_volume: float = Field(None)
    block_height: int = Field(None)
    total_supply: float = Field(None)

    quote_lp_fees: float = Field(None)
    quote_baln_fees: float = Field(None)
    base_lp_fees: float = Field(None)
    base_baln_fees: float = Field(None)

    class Config:
        extra = "ignore"


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
