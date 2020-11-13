from logging import getLogger
from app.models import User
from app.backends.mongo import MongoClient
from app.settings import (
    MONGODB_DSN,
    MONGODB_STORAGE,
    USERS_COLLECTION,
    EVENTS_COLLECTION,
)

logger = getLogger(__name__)


class UserService:
    """
    The event service abstration
    """

    def __init__(self):
        self.mongo_client = MongoClient(MONGODB_DSN, MONGODB_STORAGE)

    async def read_users(self):
        result = await self.mongo_client.do_find(USERS_COLLECTION, {})
        return result

    async def read_user(self, user_id: str):
        result = await self.mongo_client.do_find_one(USERS_COLLECTION, {"id": user_id})
        return result

    async def create_user(self, user: User):
        await self.mongo_client.do_insert_one(USERS_COLLECTION, user.dict())
        return user.dict()

    async def get_user_items(self, user_id: str):
        result = await self.mongo_client.do_find_one(
            EVENTS_COLLECTION, {"user_id": user_id}
        )
        return result
