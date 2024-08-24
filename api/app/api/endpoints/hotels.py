from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import httpx

from app.core.database import get_db
from app.schemas.hotel import RoomRequest, HotelResponse, Room
from app.models.hotel import Hotel
from app.services.availability import fetch_availability

router = APIRouter()

@router.post("/hotels", response_model=List[HotelResponse])
async def get_hotels(room_request: RoomRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Fetch hotels from the database
        result = await db.execute(select(Hotel).where(Hotel.city_id == room_request.cityId))
        hotels = result.scalars().all()

        # Fetch availability data
        try:
            availability_data = await fetch_availability(room_request)
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Error fetching availability data: {str(e)}")

        # Combine database and availability data
        combined_data = []
        for hotel in hotels:
            hotel_data = HotelResponse(
                hotel_id=hotel.hotel_id,
                hotel_name=hotel.hotel_name,
                star_rating=hotel.star_rating,
                # Add other fields as necessary
            )
            
            # Find matching live data
            live_data = next((prop for prop in availability_data["properties"] if prop["propertyId"] == hotel.hotel_id), None)
            if live_data:
                hotel_data.rooms = [
                    Room(roomId=room["roomId"], roomName=room["roomName"], price=room["totalPayment"]["inclusive"])
                    for room in live_data["rooms"]
                ]
            
            combined_data.append(hotel_data)

        return combined_data
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")