from logging import getLogger

from app.models import Item
from app.backends.mongo import MongoClient
from app.settings import (
    EVENTS_COLLECTION,
    ITEMS_COLLECTION,
    MONGODB_DSN,
    MONGODB_STORAGE,
)

logger = getLogger(__name__)


class ItemService:
    """
    The event service abstration
    """

    def __init__(self):
        self.mongo_client = MongoClient(MONGODB_DSN, MONGODB_STORAGE)

    async def read_items(self):
        result = await self.mongo_client.do_find(ITEMS_COLLECTION, {})
        return result

    async def read_item(self, item_id: str):
        result = await self.mongo_client.do_find_one(ITEMS_COLLECTION, {"id": item_id})
        return result

    async def get_item_bids(self, item_id: str):
        result = await self.mongo_client.do_find_one(
            EVENTS_COLLECTION, {"item_id": item_id}
        )
        return result

    async def create_item(self, item: Item):
        await self.mongo_client.do_insert_one(ITEMS_COLLECTION, item.dict())
        return item.dict()
