from typing import List
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, status, Depends
from uuid import UUID
from sqlmodel import Session, select
from restaurants import get_restaurant_by_id, get_restaurants_data
from schemas import Reservation, ReservationCreate, Restaurant
from database import get_database, ReservationModel
from auth import get_api_key

app = FastAPI(title="Reservation API")

@app.post("/reservations/", response_model=Reservation, status_code=status.HTTP_201_CREATED, tags=["reservations"])
def create_reservation(
    reservation: ReservationCreate, 
    session: Session = Depends(get_database),
    api_key: str = Depends(get_api_key)
) -> Reservation:
    """
    Create a new restaurant reservation.
    """
    reservation_model = ReservationModel(
        created_at=datetime.now(timezone.utc),
        customer_name=reservation.customer_name,
        party_size=reservation.party_size,
        reservation_date=reservation.reservation_date,
        restaurant_id=reservation.restaurant_id,
    )
    
    session.add(reservation_model)
    session.commit()
    session.refresh(reservation_model)
    
    restaurant_data = get_restaurant_by_id(reservation_model.restaurant_id)
    
    response_data = reservation_model.model_dump()
    response_data["restaurant"] = restaurant_data or {}
    
    return Reservation.model_validate(response_data)

@app.put("/reservations/{reservation_code}/confirm", response_model=Reservation, tags=["reservations"])
def confirm_reservation(
    reservation_code: str, 
    session: Session = Depends(get_database),
    api_key: str = Depends(get_api_key)
) -> Reservation:
    """
    Confirm an existing reservation by code.
    """
    reservation_model = session.exec(select(ReservationModel).where(ReservationModel.code == reservation_code)).one_or_none()
    if reservation_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with CODE {reservation_code} not found"
        )
    
    if reservation_model.confirmed_at:
        restaurant_data = get_restaurant_by_id(reservation_model.restaurant_id)
        response_data = reservation_model.model_dump()
        response_data["restaurant"] = restaurant_data or {}
        return Reservation.model_validate(response_data)
    
    reservation_model.confirmed_at = datetime.now(timezone.utc)
    session.add(reservation_model)
    session.commit()
    session.refresh(reservation_model)
    
    restaurant_data = get_restaurant_by_id(reservation_model.restaurant_id)
    response_data = reservation_model.model_dump()
    response_data["restaurant"] = restaurant_data or {}
    
    return Reservation.model_validate(response_data)

@app.get("/reservations/", response_model=List[Reservation], tags=["reservations"])
def list_reservations(
    session: Session = Depends(get_database),
    api_key: str = Depends(get_api_key)
) -> List[Reservation]:
    """
    List all reservations.
    """
    reservation_models = session.exec(select(ReservationModel)).all()
    
    reservations: List[Reservation] = []
    for reservation_model in reservation_models:
        restaurant_data = get_restaurant_by_id(reservation_model.restaurant_id)
        response_data = reservation_model.model_dump()
        response_data["restaurant"] = restaurant_data or {}
        reservations.append(Reservation.model_validate(response_data))
    
    return reservations

@app.get("/reservations/{reservation_code}", response_model=Reservation, tags=["reservations"])
def get_reservation(
    reservation_code: str, 
    session: Session = Depends(get_database),
    api_key: str = Depends(get_api_key)
) -> Reservation:
    """
    Get a specific reservation by CODE.
    """
    reservation_model = session.exec(select(ReservationModel).where(ReservationModel.code == reservation_code)).one_or_none()
    if reservation_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with CODE {reservation_code} not found"
        )
    
    restaurant_data = get_restaurant_by_id(reservation_model.restaurant_id)
    response_data = reservation_model.model_dump()
    response_data["restaurant"] = restaurant_data or {}
    
    return Reservation.model_validate(response_data)

@app.get("/restaurants/", response_model=List[Restaurant], tags=["restaurants"])
def list_restaurants(
    api_key: str = Depends(get_api_key)
) -> List[Restaurant]:
    """
    List all restaurants from the restaurants.json file.
    """
    restaurants_data = get_restaurants_data()
    return [Restaurant.model_validate(restaurant) for restaurant in restaurants_data]