from typing import TYPE_CHECKING
from loguru import logger

from balanced_backend.utils.api import get_token_holders, get_icx_stats
from balanced_backend.utils.rpc import get_contract_method_str
from balanced_backend.crud.tokens import get_tokens

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def run_token_stats(
        session: 'Session',
):
    logger.info("Running token stats cron...")

    tokens = get_tokens(session=session)
    for t in tokens:

        if t.address == 'ICX':
            # Not really useful info unless we want to get all the in the tracker
            t.holders = 0
            t.total_supply = get_icx_stats()['circulating-supply']
        else:
            t.holders = get_token_holders(t.address)
            total_supply = get_contract_method_str(
                to_address=t.address,
                method="totalSupply",
            )
            t.total_supply = int(total_supply, 16) / 10 ** t.decimals

        session.merge(t)
    session.commit()

    logger.info("Ending token stats cron...")


if __name__ == "__main__":
    from balanced_backend.db import session_factory

    with session_factory() as session:
        run_token_stats(session=session)
