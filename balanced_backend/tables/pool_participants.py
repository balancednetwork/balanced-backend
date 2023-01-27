from typing import Optional
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class PoolParticipant(SQLModel, table=True):
    address: Optional[str] = Field(None, primary_key=True)
    pool_id: int = Field(None, index=True)
    name: str = Field(None, index=False)
    base_amount: float = Field(None, index=False)
    quote_amount: float = Field(None, index=False)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "pool_participants"
