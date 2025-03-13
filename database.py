from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine

def generate_reservation_code():
    return f"{uuid4().hex[:6].upper()}"

class ReservationModel(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    code: str = Field(default_factory=generate_reservation_code, unique=True, index=True)
    customer_name: str
    party_size: int = Field(ge=1)
    reservation_date: datetime
    created_at: datetime
    confirmed_at: Optional[datetime] = Field(default=None, nullable=True)
    restaurant_id: int

engine = create_engine("sqlite:///database.db")


SQLModel.metadata.create_all(engine)

def get_database():
    with Session(engine) as session:
        yield session
