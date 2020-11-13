import faust
from datetime import datetime


class ValidEvent(faust.Record):
    """ The stream'd valid event """

    id: str
    item_id: str
    user_id: str
    value: float
    bid_date: datetime
    created_date: datetime
    client: str


class InvalidEvent(faust.Record):
    """The stream'd invalid event
    example: a item that has a bid of 10,000,000 $ as a joke for an item
    This can be handled on client side and the server side as well
    but i put it here to explain a use case of an invalid event
    """

    event: ValidEvent
    reason: str
