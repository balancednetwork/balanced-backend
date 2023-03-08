from typing import TYPE_CHECKING
from loguru import logger

from balanced_backend.utils.methods import build_interval_time_series
from balanced_backend.cron.method_addresses import contract_methods
from balanced_backend.models.contract_method_base import ContractMethodBase
from balanced_backend.utils.rpc import get_icx_call, get_contract_method_str
from balanced_backend.addresses import addresses

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def update_contract_methods():
    r = get_icx_call(
        to_address=addresses.LOANS_CONTRACT_ADDRESS,
        params={"method": "getCollateralTokens"}
    )
    if r.status_code == 200:
        loans_collatoral_tokens = r.json()['result']
        for _, v in loans_collatoral_tokens.items():
            symbol = get_contract_method_str(to_address=v, method="symbol")
            contract_methods.append({
                'contract_name': f'loans_{symbol}_balance',
                'params': {
                    "to": v,
                    "dataType": "call",
                    "data": {
                        "method": "balanceOf",
                        "params": {
                            "_owner": addresses.LOANS_CONTRACT_ADDRESS
                        }
                    }
                },
                'init_chart_block': 47751328,
            })
    else:
        logger.info("Failed to get loans_collatoral_tokens...")

    r = get_icx_call(
        to_address=addresses.STABILITY_FUND_CONTRACT_ADDRESS,
        params={"method": "getAcceptedTokens"}
    )
    if r.status_code == 200:
        stability_accepted_tokens = r.json()['result']
        for c in stability_accepted_tokens:
            symbol = get_contract_method_str(to_address=c, method="symbol")
            contract_methods.append({
                'contract_name': f'stability_{symbol}_balance',
                'params': {
                    "to": c,
                    "dataType": "call",
                    "data": {
                        "method": "balanceOf",
                        "params": {
                            "_owner": addresses.STABILITY_FUND_CONTRACT_ADDRESS
                        }
                    }
                },
                'init_chart_block': 47751328,
            })
    else:
        logger.info("Failed to get stability_accepted_tokens...")


def run_methods(
        session: 'Session',
):
    logger.info("Running methods cron...")
    for i in contract_methods:
        historical_method_interval = ContractMethodBase(**i)
        historical_method_interval.init_model()
        historical_method_interval.update_interval = 24 * 60 * 60
        build_interval_time_series(
            session=session,
            context=historical_method_interval,
        )
    logger.info("Ending methods cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_methods(session=session)
