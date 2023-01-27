from typing import Optional
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class Pool(SQLModel, table=True):
    base_address: Optional[str] = Field(primary_key=True, index=True)
    quote_address: Optional[str] = Field(primary_key=True, index=True)

    chain_id: int = Field(None, index=True)
    pool_id: int = Field(None, index=True)
    name: str = Field(None, index=False)
    base_name: str = Field(None, index=False)
    quote_name: str = Field(None, index=False)
    base_symbol: str = Field(None, index=False)
    quote_symbol: str = Field(None, index=False)
    base_decimals: int = Field(None, index=False)
    quote_decimals: int = Field(None, index=False)

    type: str = Field(None, index=False)

    price: float = Field(None, index=False)
    price_change_24h: float = Field(None, index=False)
    price_change_7d: float = Field(None, index=False)
    price_change_30d: float = Field(None, index=False)
    holders: int = Field(None, index=False)
    total_supply: float = Field(None, index=False)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "pools"

# TODO: RM this -> Should go in contract methods
# class PoolPrice(SQLModel, table=True):
#     base_address: Optional[str] = Field(primary_key=True)
#     quote_address: Optional[str] = Field(primary_key=True)
#     pool_id: int = Field(None, index=True)
#     name: str = Field(None, index=False)
#
#     timestamp: Optional[int] = Field(primary_key=True)
#     price: int = Field(None, index=False)
#
#     total_supply: float = Field(None, index=False)
#
#     class Config:
#         extra = "ignore"
#
#     @declared_attr
#     def __tablename__(cls) -> str:  # noqa: N805
#         return "pool_prices"
