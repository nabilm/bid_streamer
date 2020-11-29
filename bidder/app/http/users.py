from datetime import datetime
import uuid
from fastapi import APIRouter
from app.models import User
from app.service.user import UserService

router = APIRouter()
user_service = UserService()


@router.get("/users/", tags=["users"])
async def read_users():
    # This one should support pagination
    # But for simplicity it will return without pagination
    result = await user_service.read_users()
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
    result = await user_service.create(user)
    return result


@router.get("/users/{user_id}", tags=["users"])
async def read_user(user_id: str):
    """ Return a user by user id """
    result = await user_service.read_user(user_id)
    return result


@router.get("/users/items/{user_id}", tags=["users"])
async def get_user_items(user_id: str):
    """ Return the items at which the users did bid on """
    result = await user_service.get_user_items(user_id)
    return result
