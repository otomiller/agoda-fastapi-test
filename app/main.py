from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from db.db_connect import get_db_connection
from pydantic import BaseModel
from typing import List
import httpx
import os
from .database import get_db
from . import models, schemas

app = FastAPI()

API_KEY = os.getenv("API_KEY")
AGODA_API_URL = "https://sandbox-affiliateapi.agoda.com/api/v4/property/availability"

class AvailabilityRequest(BaseModel):
    checkIn: str
    checkOut: str
    rooms: int
    adults: int
    children: int
    cityId: int

async def fetch_availability(params):
    async with httpx.AsyncClient() as client:
        response = await client.get(AGODA_API_URL, params=params)
        return response.json()

@app.get("/hotels", response_model=List[schemas.Hotel])
def get_hotels_by_city(city_id: int, db: Session = Depends(get_db)):
    hotels = db.query(models.Hotel).filter(models.Hotel.city_id == city_id).all()
    return hotels

@app.get("/hotel/{hotel_id}", response_model=schemas.HotelDetail)
def get_hotel_details(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    description = db.query(models.HotelDescription).filter(models.HotelDescription.hotel_id == hotel_id).first()
    facilities = db.query(models.Facility).filter(models.Facility.hotel_id == hotel_id).all()
    rooms = db.query(models.RoomType).filter(models.RoomType.hotel_id == hotel_id).all()
    
    return schemas.HotelDetail(
        hotel=hotel,
        description=description,
        facilities=facilities,
        rooms=rooms
    )

@app.post("/hotel/availability")
async def check_hotel_availability(data: AvailabilityRequest, db: Session = Depends(get_db)):
    hotels = db.query(models.Hotel).filter(models.Hotel.city_id == data.cityId).all()
    hotel_ids = [hotel.hotel_id for hotel in hotels]
    
    params = {
        "apikey": API_KEY,
        "mdate": data.checkIn,
        "mtypeid": 1,
        "siteID": 1923846,
        "checkIn": data.checkIn,
        "checkOut": data.checkOut,
        "rooms": data.rooms,
        "adults": data.adults,
        "children": data.children,
        "propertyIds": ",".join(map(str, hotel_ids))
    }
    
    availability_data = await fetch_availability(params)
    
    results = []
    for property in availability_data.get("properties", []):
        hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == property["propertyId"]).first()
        if hotel:
            hotel_data = schemas.Hotel.from_orm(hotel)
            hotel_data.rooms = property.get("rooms", [])
            results.append(hotel_data)
    
    return results