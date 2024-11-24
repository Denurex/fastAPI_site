from datetime import date

from pydantic import BaseModel
from sqlalchemy import JSON


class SHotelsInfo(BaseModel):
    location: str
    hotel_name: str
    total_quantity: int
    total_available_rooms: int
    id: int
    image_id: int

    class Config:
        from_attributes = True


class SRoomInfo(BaseModel):
    quantity: int
    available_rooms: int
    name: str
    price: int
    services: list
    description: str

    class Config:
        from_attributes = True
