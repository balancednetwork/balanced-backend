from typing import Optional
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class Transaction(SQLModel, table=True):

    hash: Optional[str] = Field(primary_key=True, index=True)

    timestamp
    transaction_index
    from_address
    to_address
    value
    status
    step_price
    step_used
    cumulative_step_used
    data
    data_type
    score_address
    signature
    version
    method


    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "transactions"
