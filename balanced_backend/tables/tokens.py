from typing import Optional
from sqlalchemy.orm import declared_attr
from sqlalchemy.sql.schema import Column
from sqlmodel import Field, SQLModel, JSON


class Token(SQLModel, table=True):
    address: Optional[str] = Field(primary_key=True, index=True)
    chain_id: int = Field(primary_key=True, index=True)
    name: str = Field(None, index=True)
    symbol: str = Field(None, index=True)
    decimals: int = Field(None, index=False)
    logo_uri: str = Field(None, index=False)

    type: str = Field(None, index=False)
    is_stable: bool = Field(None, index=False)
    in_stability_fund: bool = Field(None, index=False)

    price: Optional[float] = Field(None, index=False)
    price_24h: float = Field(None, index=False)
    price_7d: float = Field(None, index=False)
    price_30d: float = Field(None, index=False)

    path: dict = Field(None, sa_column=Column(JSON))
    pools: dict = Field(None, sa_column=Column(JSON))

    holders: int = Field(None, index=False)
    total_supply: float = Field(None, index=False)
    liquidity: float = Field(None)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "tokens"
