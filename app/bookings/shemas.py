from datetime import date
from typing import Optional

from pydantic import BaseModel


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    tottal_cost: Optional[int] = None
    tital_days: Optional[int] = None

    class Config:
        from_attributes = True
