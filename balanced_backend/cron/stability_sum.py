from typing import TYPE_CHECKING
from loguru import logger
from sqlalchemy import text

from balanced_backend.addresses import addresses
from balanced_backend.utils.rpc import (
    get_icx_call,
    get_contract_method_str,
)

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from sqlalchemy.orm import Session


def create_replace_stability_fund_balance(session: Session, contract_names: list[str]):
    sql_query = text(f"""
    DROP MATERIALIZED VIEW IF EXISTS stability_fund_balance;

    CREATE MATERIALIZED VIEW stability_fund_balance AS
    SELECT timestamp,
           date,
           update_interval,
           COALESCE(SUM(CASE WHEN contract_name IN (
           {' ,'.join([f"'{name}'" for name in contract_names])}
           ) THEN value ELSE 0 END), 0) AS balance
    FROM daily_historicals
    WHERE contract_name IN (
    {' ,'.join([f"'{name}'" for name in contract_names])}
    ) GROUP BY timestamp, date, update_interval
    ORDER BY timestamp DESC;
    """)

    try:
        session.execute(sql_query)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating materialized view: {str(e)}")
        raise e

def build_stability_sum(session: 'Session'):
    """Sum all the stability fund."""
    logger.info(f"Starting {__name__} cron")

    # Stability fund balance of tokens
    r = get_icx_call(
        to_address=addresses.STABILITY_FUND_CONTRACT_ADDRESS,
        params={"method": "getAcceptedTokens"}
    )

    # contracts = []
    contract_names = []
    if r.status_code == 200:
        stability_accepted_tokens = r.json()['result']
        for c in stability_accepted_tokens:
            # If we normalize to usd then we do this but for now it is close enough.
            # Also this is not complete... Would need a time series of prices. To make
            # it simple we could just take the current price but then we are updating
            # whole time series at least whenever it syncs to the current price. So it
            # is all dirty... fuckit
            # contract = {}
            # contract['symbol'] = get_contract_method_str(to_address=c, method="symbol")
            # contract['decimals'] = get_contract_method_int(c, method="decimals")
            # contract['price'] = get_token_price(session, address=c)
            # contract['name'] = f"stability_{contract['symbol']}_balance"
            # contracts.append(contract)

            contract_names.append(f'stability_{get_contract_method_str(to_address=c, method="symbol")}_balance')

    create_replace_stability_fund_balance(session, contract_names)

    logger.info(f"Ending {__name__} cron")


def run_stability_sum(session: 'Session'):
    logger.info(f"Starting {__name__} cron")
    view_name = 'stability_fund_balance'
    refresh_query = text(f"REFRESH MATERIALIZED VIEW {view_name}")
    try:
        session.execute(refresh_query)
        session.commit()
        logger.info(f"Materialized view '{view_name}' refreshed successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Error refreshing materialized view '{view_name}': {str(e)}")
        raise e
    logger.info(f"Ending {__name__} cron")



if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        build_stability_sum(session=session)
