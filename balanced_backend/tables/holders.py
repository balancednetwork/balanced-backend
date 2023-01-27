from typing import Optional
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class Holder(SQLModel, table=True):

    address: str = Field(primary_key=True, index=True)
    pool_name: str = Field(None, index=True)
    pool_id: str = Field(None, index=True)
    base_address: str = Field(None, index=True)
    quote_address: str = Field(None, index=True)
    base_symbol: str = Field(None, index=True)
    quote_symbol: str = Field(None, index=True)
    quote_balance: str = Field(None, index=True)
    base_balance: str = Field(None, index=True)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "holders"
