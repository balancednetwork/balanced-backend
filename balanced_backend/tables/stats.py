from __future__ import annotations

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from sqlmodel.main import SQLModelConfig

from balanced_backend.config import settings


class Stats(SQLModel, table=True):
    chain_id: int | None = Field(settings.CHAIN_ID, primary_key=True)
    fees_earned_24h: float | None = Field(None)
    fees_earned_30d: float | None = Field(None)

    model_config = SQLModelConfig(
        extra="ignore",
    )

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "stats"
