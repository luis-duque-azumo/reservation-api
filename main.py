from typing import List
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, status, Depends
from uuid import UUID
from sqlmodel import Session, select
from schemas import Reservation, ReservationCreate
from database import get_database, ReservationModel
app = FastAPI(title="Reservation API")


@app.post("/reservations/", response_model=Reservation, status_code=status.HTTP_201_CREATED, tags=["reservations"])
def create_reservation(reservation: ReservationCreate, session: Session = Depends(get_database)) -> Reservation:
    """
    Create a new restaurant reservation.
    """
    reservation_model = ReservationModel(
        created_at=datetime.now(timezone.utc),
        customer_name=reservation.customer_name,
        party_size=reservation.party_size,
        reservation_date=reservation.reservation_date,
        confirmed=reservation.confirmed
    )
    
    session.add(reservation_model)
    session.commit()
    session.refresh(reservation_model)
    
    return Reservation.model_validate(reservation_model)

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
    
    if reservation_model.confirmed:
        return Reservation(**reservation_model.model_dump())
    
    reservation_model.confirmed = True
    session.add(reservation_model)
    session.commit()
    session.refresh(reservation_model)
    
    return Reservation(**reservation_model.model_dump())

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