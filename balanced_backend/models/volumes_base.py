from typing import Callable
from datetime import datetime
from pydantic import BaseModel

from balanced_backend.utils.time_to_block import get_timestamp_from_block


class VolumeIntervalBase(BaseModel):
    # Update once at beginning of enrichment
    address: str
    decimals: float = 1e18
    contract_name: str
    method: str

    # Can be either one of indexed position or non_indexed_position
    indexed_position: int = None
    non_indexed_position: int = None

    update_interval: int = 86400

    init_chart_time: int = None
    init_chart_block: int = None

    # Update on every value update
    start_timestamp: int = None
    end_timestamp: int = None
    days_since_launch: int = None
    date: datetime = None

    def update_time(self):
        self.date = datetime.fromtimestamp(self.start_timestamp)
        self.days_since_launch = int(
            (self.start_timestamp - self.init_chart_time) / 24 / 60 / 60)

    def init_model(self):
        if self.init_chart_time is None and self.init_chart_block:
            self.init_chart_time = get_timestamp_from_block(self.init_chart_block) / 1e6
