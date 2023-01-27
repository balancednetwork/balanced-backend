import json
from typing import Any, Type
from loguru import logger

from balanced_backend.config import settings
from balanced_backend.db import session_factory
from balanced_backend.streaming.kafka import Worker
from balanced_backend.proto.block_pb2 import Block, Transaction, Log  # noqa
from balanced_backend.addresses import addresses


def extract_method(transaction: Transaction):
    if 'method' in transaction.data:
        return json.loads(transaction.data)['method']
    else:
        return ''


class Processor(Worker):
    # Metrics
    contracts_created_python: int = 0
    contracts_updated_python: int = 0

    msg: Any = None
    data: dict = None

    block: Type[Block] = Block()
    transaction: Type[Transaction] = Transaction()
    log: Type[Log] = Log()

    def process_transaction(self):
        # Block production
        if self.transaction.to_address == '':
            return

        # Handle verification process
        if self.transaction.to_address == addresses.DEX_CONTRACT_ADDRESS:
            method = extract_method(self.transaction)
            match method:
                case "add":
                    print()

                case _:
                    logger.info("Unrecognized method")

            print()

    def process(self):
        value = self.msg.value()
        if value is None:
            return
        self.block.ParseFromString(value)

        # DEX contract was created here https://tracker.icon.community/block/33518615
        if self.block.number < 33518615:
            return

        if settings.CONSUMER_END_BLOCK is not None:
            if self.block.number > settings.CONSUMER_END_BLOCK:
                import sys
                logger.info("Finished processing batch...")
                sys.exit(0)

        for tx in self.block.transactions:
            # Filter failed Txs
            if tx.status != '0x1':
                continue

            self.transaction = tx
            self.process_transaction()
