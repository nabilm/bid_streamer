from datetime import datetime
import uuid
from fastapi import APIRouter

from app.models import Item
from app.service.item import ItemService

router = APIRouter()
item_service = ItemService()


@router.get("/items/", tags=["items"])
async def read_items():
    items = await item_service.read_items()
    return items


@router.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: str):
    result = await item_service.read_item(item_id)
    return result


@router.get("/items/bids/{item_id}", tags=["items"])
async def get_item_bids(item_id: str):
    """ Get all bids for a certain item """
    result = await item_service.get_item_bids(item_id)
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
    item = await item_service.create_item(item)
    return item
