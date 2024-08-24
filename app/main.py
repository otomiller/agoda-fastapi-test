from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db

app = FastAPI()

@app.get("/hotels", response_model=list[schemas.Hotel])
def get_hotels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    hotels = db.query(models.Hotel).offset(skip).limit(limit).all()
    return hotels

@app.get("/hotels/{hotel_id}", response_model=schemas.Hotel)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel

@app.post("/hotels", response_model=schemas.Hotel)
def create_hotel(hotel: schemas.HotelBase, db: Session = Depends(get_db)):
    db_hotel = models.Hotel(**hotel.dict())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

@app.put("/hotels/{hotel_id}", response_model=schemas.Hotel)
def update_hotel(hotel_id: int, hotel: schemas.HotelBase, db: Session = Depends(get_db)):
    db_hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    for key, value in hotel.dict().items():
        setattr(db_hotel, key, value)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

@app.delete("/hotels/{hotel_id}", response_model=schemas.Hotel)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    db.delete(db_hotel)
    db.commit()
    return db_hotel