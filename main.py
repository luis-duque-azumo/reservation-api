from typing import List, Dict
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, status
from uuid import uuid4, UUID

from schemas import Reservation, ReservationCreate

app = FastAPI(title="Reservation API")

# In-memory database
db: Dict[UUID, Reservation] = {}

@app.post("/reservations/", response_model=Reservation, status_code=status.HTTP_201_CREATED, tags=["reservations"])
def create_reservation(reservation: ReservationCreate) -> Reservation:
    """
    Create a new restaurant reservation.
    """
    reservation_id = uuid4()
    reservation_dict = reservation.model_dump()
    
    new_reservation = Reservation(
        id=reservation_id,
        created_at=datetime.now(timezone.utc),
        **reservation_dict
    )
    
    db[reservation_id] = new_reservation
    return new_reservation

@app.put("/reservations/{reservation_id}/confirm", response_model=Reservation, tags=["reservations"])
def confirm_reservation(reservation_id: UUID) -> Reservation:
    """
    Confirm an existing reservation by ID.
    """
    if reservation_id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with ID {reservation_id} not found"
        )
    
    reservation = db[reservation_id]
    reservation.confirmed = True
    db[reservation_id] = reservation
    
    return reservation

@app.get("/reservations/", response_model=List[Reservation], tags=["reservations"])
def list_reservations() -> List[Reservation]:
    """
    List all reservations.
    """
    return list(db.values())

@app.get("/reservations/{reservation_id}", response_model=Reservation, tags=["reservations"])
def get_reservation(reservation_id: UUID) -> Reservation:
    """
    Get a specific reservation by ID.
    """
    if reservation_id not in db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with ID {reservation_id} not found"
        )
    
    return db[reservation_id]