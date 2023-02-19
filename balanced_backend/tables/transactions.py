from typing import Optional
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):

    hash: Optional[str] = Field(primary_key=True, index=True)

    timestamp: int = Field(None)
    transaction_index: int = Field(None)
    from_address: str = Field(None)
    to_address: str = Field(None)
    value: float = Field(None)
    status: str = Field(None)
    step_price: int = Field(None)
    step_used: int = Field(None)
    cumulative_step_used: int = Field(None)
    data: dict = Field(None)
    data_type: str = Field(None)
    score_address: str = Field(None)
    signature: str = Field(None)
    version: str = Field(None)
    method: str = Field(None)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "transactions"
