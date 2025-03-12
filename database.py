from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import Field, Session, SQLModel, create_engine


class ReservationModel(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    customer_name: str
    party_size: int = Field(ge=1)
    reservation_date: datetime
    created_at: datetime
    confirmed: bool = False
    restaurant_id: int

engine = create_engine("sqlite:///database.db")


SQLModel.metadata.create_all(engine)

def get_database():
    with Session(engine) as session:
        yield session
