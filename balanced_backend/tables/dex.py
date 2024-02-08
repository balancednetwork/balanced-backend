from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class DexSwap(SQLModel, table=True):
    chain_id: int = Field(None, primary_key=True)
    transaction_hash: str = Field(None, primary_key=True)
    log_index: int = Field(None, primary_key=True)
    timestamp: int = Field(None, index=True)
    block_number: int = Field(None, index=True)
    pool_id: int = Field(None, index=True)

    from_token: str = Field(None)
    to_token: str = Field(None)

    base_token: str = Field(None)
    base_token_value: str = Field(None)
    base_token_value_decimal: float = Field(None)

    quote_token: str = Field(None)
    quote_token_value: str = Field(None)
    quote_token_value_decimal: float = Field(None)

    sender: str = Field(None)
    receiver: str = Field(None)
    from_value: str = Field(None)
    to_value: str = Field(None)
    lp_fees: str = Field(None)
    baln_fees: str = Field(None)
    pool_base: str = Field(None)
    pool_quote: str = Field(None)
    ending_price: str = Field(None)
    effective_fill_price: str = Field(None)

    from_value_decimal: float = Field(None)
    to_value_decimal: float = Field(None)
    lp_fees_decimal: float = Field(None)
    baln_fees_decimal: float = Field(None)
    pool_base_decimal: float = Field(None)
    pool_quote_decimal: float = Field(None)
    ending_price_decimal: float = Field(None)
    effective_fill_price_decimal: float = Field(None)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "dex_swaps"


class DexAdd(SQLModel, table=True):
    chain_id: int = Field(None, primary_key=True)
    transaction_hash: str = Field(None, primary_key=True)
    log_index: int = Field(None, primary_key=True)
    timestamp: int = Field(None, index=True)
    block_number: int = Field(None, index=True)

    pool_id: int = Field(None)
    owner: str = Field(None)
    value: str = Field(None)
    value_decimal: float = Field(None)
    base: str = Field(None)
    base_decimal: float = Field(None)
    quote: str = Field(None)
    quote_decimal: float = Field(None)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "dex_adds"
