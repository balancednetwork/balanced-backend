from sqlmodel import SQLModel, Field, Column
from pydantic import create_model
from typing import Optional
from sqlalchemy import DateTime, Integer, Float
from datetime import datetime

TIME_SERIES_CHARTS = [
    {
        'tablename': 'foo'
    }
]

models = []

for i in TIME_SERIES_CHARTS:
    models.append(create_model(
        i['tablename'].title(),
        __base__=SQLModel,
        timestamp=(Optional[int],
                   Field(default=None, primary_key=True, sa_column=Column(Integer))),
        datetime=(Optional[datetime], Field(default=None, sa_column=Column(DateTime))),
        value=(Optional[float], Field(default=None, sa_column=Column(Float))),
    ))

__all__ = models
print(models)