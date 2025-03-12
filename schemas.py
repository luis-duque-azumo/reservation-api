from uuid import UUID
from pydantic import BaseModel, Field


from datetime import datetime



class Reservation(BaseModel):
    id: UUID
    customer_name: str
    party_size: int = Field(gt=0)
    reservation_date: datetime
    created_at: datetime
    confirmed: bool = False
    class Config:
        from_attributes = True
