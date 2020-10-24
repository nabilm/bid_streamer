import faust
from streamer.models import ValidEvent, InvalidEvent
from app.backends.mongo import MongoClient
from app.settings import (
    MONGODB_DSN,
    MONGODB_STORAGE,
    ITEMS_COLLECTION,
    EVENTS_TOPIC,
    EVENTS_COLLECTION,
    KAFKA_HOST,
    EVENTS_INVALID_TOPIC,
)

app = faust.App("bids-streamer", broker="kafka://{}".format(KAFKA_HOST))
topic = app.topic(EVENTS_TOPIC, value_type=ValidEvent)
invalid_topic = app.topic(EVENTS_INVALID_TOPIC, value_type=InvalidEvent)
mongo_client = MongoClient(MONGODB_DSN, MONGODB_STORAGE)
# FAUST table to keep the winning bid, this table can be sharded as well
winning_bid_table = app.Table("winning_bids", default=float)


@app.agent(topic)
async def process_events(events):
    async for event in events:
        # A use case for having the invalid topic

        if event.value > 100000:
            invalid_event = InvalidEvent(
                event=event, reason="Value bigger than threshold"
            )
            invalid_topic.send(value=invalid_event)
            continue
        if winning_bid_table[event.item_id] < event.value:
            winning_bid_table[event.item_id] = event.value
        # Flow the event in mongodb async
        await mongo_client.do_insert_one(EVENTS_COLLECTION, event.asdict())
        # Assuming that you can't bid less than the current bid
        await mongo_client.do_update_one(
            ITEMS_COLLECTION,
            id=event.item_id,
            query={"$set": {"winning_bid": winning_bid_table[event.item_id]}},
        )


if __name__ == "__main__":
    app.main()
