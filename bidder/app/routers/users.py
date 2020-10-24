from datetime import datetime
import uuid
from fastapi import APIRouter

from app.models import User
from app.backends.mongo import MongoClient
from app.settings import (
    MONGODB_DSN,
    MONGODB_STORAGE,
    USERS_COLLECTION,
    EVENTS_COLLECTION,
)

router = APIRouter()
mongo_client = MongoClient(MONGODB_DSN, MONGODB_STORAGE)


@router.get("/users/", tags=["users"])
async def read_users():
    # This one should support pagination
    # But for simplicity it will return without pagination
    result = await mongo_client.do_find(USERS_COLLECTION, {})
    return result


@router.post("/users/", tags=["users"])
async def create_user(user: User):
    """
    Create a userid
    note: user ids are created here in order to decouple the models with
    specific engine or type of id
    but if we are sure that we will be always using mongodb then
    Object id creation and handling need to be in the model
    """
    user.id = str(uuid.uuid4())
    user.created_date = datetime.now()
    await mongo_client.do_insert_one(USERS_COLLECTION, user.dict())
    return user.dict()


@router.get("/users/{user_id}", tags=["users"])
async def read_user(user_id: str):
    """ Return a user by user id """
    result = await mongo_client.do_find_one(USERS_COLLECTION, {"id": user_id})
    return result


@router.get("/users/items/{user_id}", tags=["users"])
async def get_user_items(user_id: str):
    """ Return the items at which the users did bid on """
    result = await mongo_client.do_find_one(EVENTS_COLLECTION, {"user_id": user_id})
    return result
