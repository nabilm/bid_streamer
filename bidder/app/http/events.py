from datetime import datetime
import uuid
from fastapi import APIRouter
from app.service.event import EvenService
from app.models import Event

event_service = EvenService()
router = APIRouter()


@router.get("/events/", tags=["events"])
async def read_events():
    # This one should support pagination
    # But for simplicity it will return without pagination
    result = await event_service.read_event()
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
    result = await event_service.create_event(event)

    return result
