from typing import TYPE_CHECKING
from loguru import logger

from balanced_backend.utils.streaming import extract_method_from_tx, extract_tx_log, extract_method_from_log
from balanced_backend.tables.dex import DexSwap
from balanced_backend.utils.pools import get_cached_pool_id

if TYPE_CHECKING:
    from balanced_backend.proto.block_pb2 import Log, Transaction, Block  # noqa
    from sqlalchemy.orm import Session


# def process_dex_add(transaction: 'Transaction') -> DexSwap:
#     logs = transaction.logs
#
#     base_token_volume = logs['data'][5]
#
#     # model = DexSwap(
#     #     transaction_hash=transaction.hash,
#     #     timestamp=transaction.timestamp,
#     #     base_token_volume=transaction.base_token_volume,
#     #     block_number=transaction.,
#     #     closing_price=transaction.,
#     #     market_id=transaction.,
#     #     target_token_volume=transaction.,
#     #     type=transaction.,
#     # )
#
#
# def process_dex_tx(session: Session, transaction: 'Transaction'):
#     model = None
#     method = extract_method_from_tx(transaction)
#     match method:
#         case "add":
#             model = process_dex_add(transaction=transaction)
#
#         case _:
#             logger.info(f"Unrecognized dex method {method}...")
#
#     if model is not None:
#         session.merge(model)
#         session.commit()


# def transform_dex_swap_log(block: 'Block', tx_index: int, log_index: int) -> DexSwap:
#     tx, log = extract_tx_log(block=block, tx_index=tx_index, log_index=log_index)
#
#     swap = DexSwap(
#         transaction_hash=tx.hash,
#         block_number=block.number,
#         market_id=get_cached_pool_id(
#             base_address=log.data[0],
#             quote_address=log.data[1],
#         ),
#         timestamp=tx.timestamp,
#         base_token_volume=0,
#     )
#
#     return swap


def process_dex_log(session: 'Session', block: 'Block', tx_index: int, log_index: int):
    table = None
    match extract_method_from_log(block.transaction[tx_index].log[log_index]):
        case 'Swap':
            # table = transform_dex_swap_log(
            #     block=block,
            #     tx_index=tx_index,
            #     log_index=log_index
            # )
            pass

    if table is not None:
        session.merge(table)
        session.commit()

