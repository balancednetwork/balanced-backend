from typing import Optional
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class Token(SQLModel, table=True):
    address: Optional[str] = Field(primary_key=True, index=True)
    chain_id: int = Field(primary_key=True, index=True)
    name: str = Field(None, index=False)
    symbol: str = Field(None, index=False)
    decimals: int = Field(None, index=False)
    logo_uri: str = Field(None, index=False)

    type: str = Field(None, index=False)

    price: Optional[float] = Field(None, index=False)
    price_24h: float = Field(None, index=False)
    price_7d: float = Field(None, index=False)
    price_30d: float = Field(None, index=False)
    holders: int = Field(None, index=False)
    total_supply: float = Field(None, index=False)

    volume: str = Field(None)
    volume_decimal: str = Field(None)

    lp_fees: str = Field(None)
    lp_fees_decimal: float = Field(None)
    baln_fees: str = Field(None)
    baln_fees_decimal: float = Field(None)


    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "tokens"


class TokenPool(SQLModel, table=True):
    pool_id: int = Field(primary_key=True)
    chain_id: int = Field(None, index=True)
    timestamp: int = Field(None)
    pool_price: float = Field(None)
    pool_name: str = Field(None)
    total_supply: float = Field(None)
    address: str = Field(primary_key=True)
    symbol: str = Field(None, index=True)
    name: str = Field(None)
    price: Optional[float] = Field(None)
    supply: Optional[float] = Field(None)
    reference_address: str = Field(None, index=True)
    reference_symbol: str = Field(None, index=True)
    reference_name: str = Field(None)
    reference_price: float = Field(None)
    reference_supply: float = Field(None)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "token_pool"


class TokenPrice(SQLModel, table=True):
    name: Optional[str] = Field(primary_key=True)
    chain_id: int = Field(None, index=True)
    timestamp: Optional[int] = Field(primary_key=True)
    price: float = Field(None, index=False)
    total_supply: float = Field(None, index=False)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "token_prices"
