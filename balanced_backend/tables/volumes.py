from typing import NewType, Union
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class ContractMethodVolume(SQLModel, table=True):
    address: str = Field(primary_key=True)
    method: str = Field(primary_key=True)

    contract_name: str = Field(None, index=True)

    start_timestamp: int = Field(primary_key=True)
    end_timestamp: int = Field(primary_key=True)

    start_date: datetime = Field(None, index=True,
                                 sa_column=sa.Column(sa.DateTime(timezone=True)))
    end_date: datetime = Field(None, index=True,
                               sa_column=sa.Column(sa.DateTime(timezone=True)))

    start_block: int
    end_block: int
    update_interval: int = Field(None, index=True)
    days_since_launch: int = Field(None, index=True)
    value: float
    num_events: int

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "contract_method_volumes"


class VolumeBase(SQLModel):
    chain_id: int = Field(None, primary_key=True)
    pool_id: int = Field(None, primary_key=True)
    timestamp: int = Field(None, primary_key=True)

    close: float = Field(None)
    open: float = Field(None)
    high: float = Field(None)
    low: float = Field(None)

    base_volume: float = Field(None)
    quote_volume: float = Field(None)

    lp_fees: float = Field(None)
    baln_fees: float = Field(None)

    # block_start: int = Field(None)
    # block_end: int = Field(None)
    #
    # price_decimal: float = Field(None)
    # base_price_decimal: float = Field(None)
    # quote_price_decimal: float = Field(None)
    # volume_decimal: float = Field(None)
    # lp_fees_decimal: float = Field(None)
    # baln_fees_decimal: float = Field(None)

    class Config:
        extra = "ignore"


class VolumeSeries5Min(VolumeBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "volume_series_5_min"


class VolumeSeries15Min(VolumeBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "volume_series_15_min"


class VolumeSeries1Hour(VolumeBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "volume_series_1_hour"


class VolumeSeries4Hour(VolumeBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "volume_series_4_hour"


class VolumeSeries1Day(VolumeBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "volume_series_1_day"


class VolumeSeries1Week(VolumeBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "volume_series_1_week"


class VolumeSeries1Month(VolumeBase, table=True):
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "volume_series_1_month"



VolumeTableType = NewType(
    'TableType',
    Union[
        VolumeSeries5Min,
        VolumeSeries15Min,
        VolumeSeries1Hour,
        VolumeSeries4Hour,
        VolumeSeries1Day,
        VolumeSeries1Month,
    ]
)