from typing import TYPE_CHECKING

from balanced_backend.utils.methods import build_interval_time_series
from balanced_backend.workers.method_addresses import contract_methods
from balanced_backend.models.contract_method_base import ContractMethodBase

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def build_methods(
        session: 'Session',
):
    for i in contract_methods:
        historical_method_interval = ContractMethodBase(**i)
        historical_method_interval.init_model()
        historical_method_interval.update_interval = 24 * 60 * 60
        build_interval_time_series(
            session=session,
            context=historical_method_interval,
        )
