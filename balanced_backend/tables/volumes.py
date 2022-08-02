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
