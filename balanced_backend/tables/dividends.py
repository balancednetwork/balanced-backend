from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class Dividend(SQLModel, table=True):

    chain_id: int = Field(None, primary_key=True)
    pool_id: int = Field(None, primary_key=True)
    base_address: str = Field(None, index=True)
    quote_address: str = Field(None, index=True)

    base_lp_fees_24h: float = Field(None)
    quote_lp_fees_24h: float = Field(None)
    base_baln_fees_24h: float = Field(None)
    quote_baln_fees_24h: float = Field(None)
    base_volume_24h: float = Field(None)
    quote_volume_24h: float = Field(None)

    base_lp_fees_30d: float = Field(None)
    quote_lp_fees_30d: float = Field(None)
    base_baln_fees_30d: float = Field(None)
    quote_baln_fees_30d: float = Field(None)
    base_volume_30d: float = Field(None)
    quote_volume_30d: float = Field(None)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "dividends"
