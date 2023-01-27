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

    price: float = Field(None, index=False)
    price_24h: float = Field(None, index=False)
    price_7d: float = Field(None, index=False)
    price_30d: float = Field(None, index=False)
    holders: int = Field(None, index=False)
    total_supply: float = Field(None, index=False)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "tokens"


class TokenPrice(SQLModel, table=True):
    address: Optional[str] = Field(primary_key=True)
    timestamp: Optional[int] = Field(primary_key=True)
    price: float = Field(None, index=False)
    total_supply: float = Field(None, index=False)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "token_prices"
