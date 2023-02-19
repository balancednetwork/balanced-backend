from typing import Any, Type
from loguru import logger

from balanced_backend.config import settings
from balanced_backend.streaming.kafka import Worker
from balanced_backend.proto.block_pb2 import Block, Transaction, Log  # noqa
from balanced_backend.addresses import addresses

from balanced_backend.utils.streaming import extract_method_from_log
from balanced_backend.streaming.contracts.dex import process_dex_log

class Processor(Worker):
    # Metrics
    contracts_created_python: int = 0
    contracts_updated_python: int = 0

    msg: Any = None
    data: dict = None

    block: Type[Block] = Block()
    # transaction: Type[Transaction] = Transaction()
    # log: Type[Log] = Log()

    tx_index: int = None
    log_index: int = None

    def process_transaction(self):
        match self.block.transaction[self.tx_index].to_address:
            case addresses.DEX_CONTRACT_ADDRESS:
                pass

    def process_log(self):
        match self.block.transaction[self.tx_index].log[self.log_index].address:
            case addresses.DEX_CONTRACT_ADDRESS:
                process_dex_log(
                    session=self.session,
                    block=self.block,
                    tx_index=self.tx_index,
                    log_index=self.log_index
                )

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

        for tx_index, _ in enumerate(self.block.transactions):
            # Filter failed Txs
            if self.block.transactions[tx_index].status != '0x1':
                continue

            # Block production
            if self.block.transactions[tx_index].to_address == '':
                continue

            self.tx_index = tx_index
            self.process_transaction()

            for log_index, _ in enumerate(self.block.transaction[self.tx_index].log):
                self.log_index = log_index
                self.process_log()
