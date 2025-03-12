from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional

from datetime import datetime

class Restaurant(BaseModel):
    id: int
    name: str
    cuisine: str
    price_range: str


class ReservationCreate(BaseModel):
    customer_name: str
    party_size: int = Field(gt=0)
    reservation_date: datetime
    restaurant_id: int

class Reservation(BaseModel):
    id: UUID
    customer_name: str
    party_size: int = Field(gt=0)
    reservation_date: datetime
    created_at: datetime
    confirmed_at: Optional[datetime] = Field(default=None, nullable=True)
    restaurant: Restaurant
    class Config:
        from_attributes = True

