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

from typing import List, Optional
from pydantic import BaseModel, Field

class AvailabilityRequest(BaseModel):
    checkIn: str
    checkOut: str
    rooms: int
    adults: int
    children: int
    cityId: int
    childrenAges: Optional[List[int]] = Field(default_factory=list)
    language: str = "en-us"
    currency: str = "USD"
    userCountry: str = "US"

async def fetch_availability(payload):
    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/json", "ApiKey": API_KEY}
        response = await client.post(AGODA_API_URL, json=payload, headers=headers)
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
    
    payload = {
        "waitTime": 60,
        "criteria": {
            "propertyIds": hotel_ids,
            "checkIn": data.checkIn,
            "checkOut": data.checkOut,
            "rooms": data.rooms,
            "adults": data.adults,
            "children": data.children,
            "childrenAges": data.childrenAges,
            "language": data.language,
            "currency": data.currency,
            "userCountry": data.userCountry
        },
        "features": {
            "ratesPerProperty": 25,
            "extra": [
                "content",
                "surchargeDetail",
                "CancellationDetail",
                "BenefitDetail",
                "dailyRate",
                "taxDetail",
                "rateDetail",
                "promotionDetail"
            ]
        }
    }
    
    availability_data = await fetch_availability(payload)
    
    results = []
    for property in availability_data.get("properties", []):
        hotel = db.query(models.Hotel).filter(models.Hotel.hotel_id == property["propertyId"]).first()
        if hotel:
            hotel_data = schemas.Hotel.from_orm(hotel)
            hotel_data.rooms = property.get("rooms", [])
            results.append(hotel_data)
    
    return results