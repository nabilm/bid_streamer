from logging import getLogger
from fastapi import HTTPException
from confluent_kafka import KafkaException

from app.models import Event
from app.backends.mongo import MongoClient
from app.backends.kafka import AsyncProducer
from app.settings import (
    EVENTS_COLLECTION,
    KAFKA_HOST,
    MONGODB_DSN,
    MONGODB_STORAGE,
    EVENTS_TOPIC,
)

logger = getLogger(__name__)


class EvenService:
    """
    The event service abstration
    """

    def __init__(self):
        self.mongo_client = MongoClient(MONGODB_DSN, MONGODB_STORAGE)
        self.config = config = {"bootstrap.servers": KAFKA_HOST}
        self.aio_producer = AsyncProducer(config)
        self.cnt = 0

    def _ack(self, err: Exception, msg: str):
        """
        Kafka ack method
        """
        self.cnt = self.cnt + 1

    async def read_events(self):
        result = await self.mongo_client.do_find(EVENTS_COLLECTION, {})
        return result

    async def create_event(self, event: Event):
        """
        This API write the data into Kafka topic that will be stream'd
        """
        try:
            await self.aio_producer.produce_with_delivery(
                EVENTS_TOPIC, event.json(), on_delivery=self.ack
            )
        except KafkaException as ex:
            raise HTTPException(status_code=500, detail=ex.args[0].str())
        return event.dict()
