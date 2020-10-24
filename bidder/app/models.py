"""
Bidder app models which will be used both in event
streaming and the API
"""
from datetime import datetime
from pydantic import BaseModel, Field


class User(BaseModel):
    """ Limited user profile by name """

    id: str = None
    name: str
    bids: int = 0

    class Config:
        allow_population_by_field_name = True

    created_date: datetime = None


class Item(BaseModel):
    id: str = Field(None, alias="_id")
    name: str
    init_bid: float
    winning_bid: float = 0
    currency: str = "EUR"
    created_date: datetime
    bids: int = 0
    pictures: list = []
    bidding_enddate: datetime


class Event(BaseModel):
    id: str = Field(None, alias="_id")
    item_id: str
    user_id: str
    value: float
    bid_date: datetime
    created_date: datetime = datetime.now()
    client: str = "web"
