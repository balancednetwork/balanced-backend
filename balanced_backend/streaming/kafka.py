from time import sleep
from typing import Any

from confluent_kafka import Consumer, KafkaError, Message
from confluent_kafka.admin import AdminClient

from loguru import logger
from pydantic import BaseModel

from balanced_backend.config import settings


class Worker(BaseModel):
    name: str = None

    session: Any = None
    partition_dict: dict = None

    kafka_server: str = settings.KAFKA_BROKER_URL
    consumer_group: str = settings.CONSUMER_GROUP
    auto_offset_reset: str = settings.CONSUMER_AUTO_OFFSET_RESET

    topic: str = settings.CONSUMER_TOPIC_BLOCKS
    msg_count: int = 0

    consumer: Any = None
    msg: Message = None
    check_topics: bool = True

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.consumer = Consumer(
            {
                "bootstrap.servers": self.kafka_server,
                "group.id": self.consumer_group,
                # Offset determined by worker type head (latest) or tail (earliest)
                "auto.offset.reset": self.auto_offset_reset,
            }
        )

        if self.check_topics:
            admin_client = AdminClient({"bootstrap.servers": self.kafka_server})
            topics = admin_client.list_topics().topics

            if self.topic and self.topic not in topics:
                # Used as bare producer as well
                raise RuntimeError(f"Topic {self.topic} not in {topics}")

    def start(self):
        self.consumer.subscribe([self.topic])
        logger.info(f"Kafka consumer connected to consumer group = {settings.CONSUMER_GROUP}...")

        while True:
            # Poll for a message
            msg = self.consumer.poll(timeout=1)

            # If no new message, try again
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    logger.error(
                        f"Kafka consumer: Kafka topic {msg.topic()} not ready. Restarting."
                    )
                elif msg.error():
                    logger.error("Kafka consumer: " + str(msg.error()))
                sleep(1)
                continue
            else:
                self.msg = msg
                self.msg_count += 1
                self.process()


    def process(self):
        raise Exception("Should have overriden the process method...")
