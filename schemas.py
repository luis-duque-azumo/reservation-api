from uuid import UUID
from pydantic import BaseModel, Field


from datetime import datetime



class ReservationCreate(BaseModel):
    customer_name: str
    party_size: int = Field(gt=0)
    reservation_date: datetime
    confirmed: bool = False

class Reservation(BaseModel):
    id: UUID
    customer_name: str
    party_size: int = Field(gt=0)
    reservation_date: datetime
    created_at: datetime
    confirmed: bool = False
    class Config:
        from_attributes = True

class Restaurant(BaseModel):
    id: int
    name: str
    cuisine: str
    price_range: str
