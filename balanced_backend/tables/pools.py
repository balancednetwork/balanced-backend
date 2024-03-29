from typing import Optional
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class Pool(SQLModel, table=True):
    base_address: Optional[str] = Field(primary_key=True, index=True)
    quote_address: Optional[str] = Field(primary_key=True, index=True)

    chain_id: int = Field(None, index=True)
    pool_id: int = Field(None, index=True)
    name: str = Field(None, index=True)
    base_name: str = Field(None, index=True)
    quote_name: str = Field(None, index=True)
    base_symbol: str = Field(None, index=True)
    quote_symbol: str = Field(None, index=True)
    base_decimals: int = Field(None)
    quote_decimals: int = Field(None)

    type: str = Field(None, index=True)

    price: float = Field(None)
    price_24h: float = Field(None)
    price_7d: float = Field(None)
    price_30d: float = Field(None)

    price_change_24h: float = Field(None)
    price_change_7d: float = Field(None)
    price_change_30d: float = Field(None)

    price_24h_low: float = Field(None)
    price_24h_high: float = Field(None)

    base_volume_24h: float = Field(None)
    quote_volume_24h: float = Field(None)
    base_lp_fees_24h: float = Field(None)
    quote_lp_fees_24h: float = Field(None)
    base_baln_fees_24h: float = Field(None)
    quote_baln_fees_24h: float = Field(None)

    base_volume_30d: float = Field(None)
    quote_volume_30d: float = Field(None)
    base_lp_fees_30d: float = Field(None)
    quote_lp_fees_30d: float = Field(None)
    base_baln_fees_30d: float = Field(None)
    quote_baln_fees_30d: float = Field(None)

    base_price: float = Field(None)
    quote_price: float = Field(None)
    base_supply: float = Field(None)
    quote_supply: float = Field(None)
    base_liquidity: float = Field(None)
    quote_liquidity: float = Field(None)

    holders: int = Field(None)
    total_supply: float = Field(None)
    last_updated_timestamp: int = Field(None)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "pools"
