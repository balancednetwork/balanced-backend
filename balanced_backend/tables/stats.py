from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel

from balanced_backend.config import settings


class Stats(SQLModel, table=True):
    chain_id: int = Field(settings.CHAIN_ID, primary_key=True)
    fees_earned_24h: float = Field(None)
    fees_earned_30d: float = Field(None)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "stats"
