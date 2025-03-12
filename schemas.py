from uuid import UUID
from pydantic import BaseModel, Field


from datetime import datetime


class ReservationBase(BaseModel):
    customer_name: str
    party_size: int = Field(gt=0)
    reservation_date: datetime


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: UUID
    created_at: datetime
    confirmed: bool = False
    class Config:
        from_attributes = True
