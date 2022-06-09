from typing import TYPE_CHECKING
from balanced_backend.utils.historical import build_time_series
from balanced_backend.models.bnusd_supply_chart import BnusdSupplyChart
from balanced_backend.config import settings
from balanced_backend.utils.rpc import bnusd_totalSupply

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def build_bnusd_supply(session: 'Session'):
    build_time_series(
        session=session,
        rpc_call=bnusd_totalSupply,
        Model=BnusdSupplyChart,
        init_chart_time=settings.LOANS_START_TIME,
    )
