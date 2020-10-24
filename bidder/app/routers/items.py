from datetime import datetime
import uuid
from fastapi import APIRouter

from app.models import Item
from app.backends.mongo import MongoClient
from app.settings import (
    MONGODB_DSN,
    MONGODB_STORAGE,
    ITEMS_COLLECTION,
    EVENTS_COLLECTION,
)

router = APIRouter()
mongo_client = MongoClient(MONGODB_DSN, MONGODB_STORAGE)


@router.get("/items/", tags=["items"])
async def read_items():
    items = await mongo_client.do_find(ITEMS_COLLECTION, {})
    return items


@router.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: str):
    result = await mongo_client.do_find_one(ITEMS_COLLECTION, {"id": item_id})
    return result


@router.get("/items/bids/{item_id}", tags=["items"])
async def get_item_bids(item_id: str):
    """ Get all bids for a certain item """
    result = await mongo_client.do_find_one(EVENTS_COLLECTION, {"item_id": item_id})
    return result


@router.post("/items/", tags=["items"])
async def create_item(item: Item):
    """
    Create a item id
    note: user ids are created here in order to decouple the models with
    specific engine or type of id
    but if we are sure that we will be always using mongodb then
    Object id creation and handling need to be in the model
    """
    item.id = str(uuid.uuid4())
    item.created_date = datetime.now()
    await mongo_client.do_insert_one(ITEMS_COLLECTION, item.dict())
    return item.dict()
