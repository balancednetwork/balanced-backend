from datetime import datetime
from pydantic import BaseModel, validator, Field
from sqlmodel import SQLModel

from balanced_backend.utils.time_to_block import get_timestamp_from_block


class Params(BaseModel):
    to: str
    dataType: str
    data: dict

    @validator('data')
    def check_params_is_valid(cls, v):
        if 'method' not in v:
            raise ValueError("data field should have a method.")
        return v


class ContractMethodBase(BaseModel):
    params: Params

    init_chart_time: int = None
    init_chart_block: int = None

    update_interval: int = None

    # Update on every value update
    timestamp: int = None
    days_since_launch: int = None
    date: datetime = None

    # Update once at beginning of enrichment
    method: str = None
    address: str = None
    contract_name: str = None

    model: SQLModel = None
    decimals: int = Field(18)

    def update_time(self):
        self.date = datetime.fromtimestamp(self.timestamp)
        self.days_since_launch = int(
            (self.timestamp - self.init_chart_time) / 24 / 60 / 60)

    def init_model(self):
        self.method = self.params.data['method']
        self.address = self.params.to

        if self.init_chart_time is None and self.init_chart_block:
            self.init_chart_time = int(
                get_timestamp_from_block(self.init_chart_block) / 1e6
            )
