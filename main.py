from typing import List, Dict
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, status, Depends
from uuid import uuid4, UUID
from sqlmodel import Session, select
from schemas import Reservation
from database import get_database, ReservationModel
app = FastAPI(title="Reservation API")

# In-memory database
db: Dict[UUID, Reservation] = {}

@app.post("/reservations/", response_model=Reservation, status_code=status.HTTP_201_CREATED, tags=["reservations"])
def create_reservation(reservation: Reservation, session: Session = Depends(get_database)) -> Reservation:
    """
    Create a new restaurant reservation.
    """
    reservation = Reservation(
        id=uuid4(),
        created_at=datetime.now(timezone.utc),
        customer_name=reservation.customer_name,
        party_size=reservation.party_size,
        reservation_date=reservation.reservation_date
    )
    reservation_model = ReservationModel(**reservation.model_dump())
    session.add(reservation_model)
    session.commit()
    session.refresh(reservation_model)
    return reservation

@app.put("/reservations/{reservation_id}/confirm", response_model=Reservation, tags=["reservations"])
def confirm_reservation(reservation_id: UUID, session: Session = Depends(get_database)) -> Reservation:
    """
    Confirm an existing reservation by ID.
    """
    reservation_model = session.exec(select(ReservationModel).where(ReservationModel.id == reservation_id)).one_or_none()
    if reservation_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with ID {reservation_id} not found"
        )
    
    reservation = Reservation(**reservation_model.model_dump())
    reservation.confirmed = True
    
    return reservation

@app.get("/reservations/", response_model=List[Reservation], tags=["reservations"])
def list_reservations(session: Session = Depends(get_database)) -> List[Reservation]:
    """
    List all reservations.
    """
    reservation_models = session.exec(select(ReservationModel)).all()
    return [Reservation(**reservation_model.model_dump()) for reservation_model in reservation_models]

@app.get("/reservations/{reservation_id}", response_model=Reservation, tags=["reservations"])
def get_reservation(reservation_id: UUID, session: Session = Depends(get_database)) -> Reservation:
    """
    Get a specific reservation by ID.
    """
    reservation_model = session.exec(select(ReservationModel).where(ReservationModel.id == reservation_id)).one_or_none()
    if reservation_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with ID {reservation_id} not found"
        )
    
    return Reservation(**reservation_model.model_dump())