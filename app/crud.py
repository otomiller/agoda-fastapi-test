from sqlalchemy.orm import Session
from . import models

def get_hotel(db: Session, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()

def get_hotels(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Hotel).offset(skip).limit(limit).all()