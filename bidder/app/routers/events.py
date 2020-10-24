from datetime import datetime
import uuid
from fastapi import APIRouter
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

router = APIRouter()
mongo_client = MongoClient(MONGODB_DSN, MONGODB_STORAGE)

config = {
    "bootstrap.servers": KAFKA_HOST,
}
aio_producer = AsyncProducer(config)
cnt = 0


def ack(err: Exception, msg: str):
    global cnt
    cnt = cnt + 1


@router.get("/events/", tags=["events"])
async def read_event():
    # This one should support pagination
    # But for simplicity it will return without pagination
    result = await mongo_client.do_find(EVENTS_COLLECTION, {})
    return result


@router.post("/events/", tags=["events"])
async def create_event(event: Event):
    """
    Create an event id
    note: user ids are created here in order to decouple the models with
    specific engine or type of id
    but if we are sure that we will be always using mongodb then
    Object id creation and handling need to be in the model

    This API write the data into Kafka topic that will be stream'd
    """
    event.id = str(uuid.uuid4())
    event.created_date = datetime.now()
    try:
        await aio_producer.produce_with_delivery(
            EVENTS_TOPIC, event.json(), on_delivery=ack
        )
    except KafkaException as ex:
        raise HTTPException(status_code=500, detail=ex.args[0].str())

    return event.dict()
