# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from sqlalchemy.exc import SQLAlchemyError
# from typing import List
# import httpx
# import traceback

# from app.core.database import get_db
# from app.schemas.hotel import RoomRequest, HotelResponse, Room
# from app.models.hotel import Hotel
# from app.services.availability import fetch_availability

# router = APIRouter()

# @router.post("/hotels", response_model=List[HotelResponse])
# async def get_hotels(room_request: RoomRequest, db: AsyncSession = Depends(get_db)):
#     try:
#         # Fetch hotels from the database
#         result = await db.execute(select(Hotel).where(Hotel.city_id == room_request.cityId))
#         hotels = result.scalars().all()

#         # Fetch availability data
#         availability_data = await fetch_availability(room_request)

#         # Combine database and availability data
#         combined_data = []
#         for hotel in hotels:
#             hotel_data = HotelResponse(
#                 hotel_id=hotel.hotel_id,
#                 hotel_name=hotel.hotel_name,
#                 star_rating=hotel.star_rating,
#                 rooms=[]  # Initialize with an empty list
#             )
            
#             # Find matching live data
#             live_data = next((prop for prop in availability_data.get("properties", []) if prop["propertyId"] == str(hotel.hotel_id)), None)
#             if live_data:
#                 hotel_data.rooms = [
#                     Room(roomId=room["roomId"], roomName=room["roomName"], price=room["totalPayment"]["inclusive"])
#                     for room in live_data.get("rooms", [])
#                 ]
            
#             combined_data.append(hotel_data)

#         return combined_data
#     except SQLAlchemyError as e:
#         print(f"Database error: {e}")
#         print(traceback.format_exc())
#         raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         print(traceback.format_exc())
#         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
import logging

from app.core.database import get_db
from app.schemas.hotel import RoomRequest, HotelResponse, Room, HotelListResponse
from app.services.hotels import fetch_hotel_list
from app.services.availability import fetch_availability

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/hotels", response_model=HotelListResponse)
async def get_hotels(room_request: RoomRequest, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Fetching hotels for city ID: {room_request.cityId}")
        hotels = await fetch_hotel_list(room_request.cityId)

        if not hotels:
            logger.warning(f"No hotels found for the city ID: {room_request.cityId}")
            return HotelListResponse(hotels=[], message=f"No hotels found for the city ID: {room_request.cityId}")

        hotel_ids = [hotel['hotel_id'] for hotel in hotels]
        logger.info(f"Fetching availability for {len(hotel_ids)} hotels")
        
        try:
            availability_data = await fetch_availability(room_request, hotel_ids)
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            logger.error(f"Response content: {e.response.text if e.response else 'No response content'}")
            raise HTTPException(status_code=500, detail=f"Error fetching availability data: {str(e)}")

        logger.info("Combining hotel and availability data")
        combined_data = []
        for hotel in hotels:
            hotel_data = HotelResponse(
                hotel_id=hotel['hotel_id'],
                hotel_name=hotel['hotel_name'],
                star_rating=hotel['star_rating'],
            )
            
            live_data = next((prop for prop in availability_data.get("properties", []) if prop["propertyId"] == hotel['hotel_id']), None)
            if live_data:
                hotel_data.rooms = [
                    Room(roomId=room["roomId"], roomName=room["roomName"], price=room["totalPayment"]["inclusive"])
                    for room in live_data.get("rooms", [])
                ]
            
            combined_data.append(hotel_data)

        logger.info(f"Returning {len(combined_data)} hotels with availability data")
        return HotelListResponse(hotels=combined_data)
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")