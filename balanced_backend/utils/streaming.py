import json

from balanced_backend.proto.block_pb2 import Log, Transaction, Block  # noqa

def extract_method_from_tx(transaction: Transaction):
    if 'method' in transaction.data:
        return json.loads(transaction.data)['method']
    else:
        return ''


def extract_method_from_log(log: Log) -> str:
    return log.Indexed[0].split("(")[0]


def extract_tx_log(block: 'Block', tx_index: int, log_index: int) -> (Transaction, Log):
    tx = block.transactions[tx_index]
    return tx, tx.logs[log_index]
