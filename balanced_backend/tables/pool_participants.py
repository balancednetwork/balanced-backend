from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel
from sqlmodel.main import SQLModelConfig


class PoolParticipant(SQLModel, table=True):
    address: Optional[str] = Field(None, primary_key=True)
    pool_id: int | None = Field(None, index=True)
    name: str | None = Field(None, index=False)
    base_amount: float | None = Field(None, index=False)
    quote_amount: float | None = Field(None, index=False)

    model_config = SQLModelConfig(
        extra="ignore",
    )

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "pool_participants"
