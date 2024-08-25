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
from app.services.hotel import get_hotels_from_db, save_search_result
from app.services.availability import fetch_availability, sandbox_hotel_ids

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/hotels", response_model=HotelListResponse)
async def get_hotels(room_request: RoomRequest, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Fetching hotels for city ID: {room_request.cityId}")
        hotels = await get_hotels_from_db(db, room_request.cityId)

        if not hotels:
            logger.warning(f"No hotels found for the city ID: {room_request.cityId}")
            return HotelListResponse(hotels=[], message=f"No hotels found for the city ID: {room_request.cityId}")

        logger.info(f"Fetching availability for sandbox hotels")
        
        try:
            availability_data = await fetch_availability(room_request)
            if "error" in availability_data:
                logger.error(f"Error in fetch_availability: {availability_data['error']}")
                raise HTTPException(status_code=500, detail=f"Error fetching availability data: {availability_data['error']}")
            logger.info(f"Availability data received for {len(availability_data.get('properties', []))} properties")
            
            # Save the search result to the database
            search_id = availability_data.get('searchId', str(room_request.cityId))  # Use cityId as fallback if searchId is not present
            try:
                await save_search_result(db, search_id, availability_data)
                logger.info(f"Search result saved with search ID: {search_id}")
            except SQLAlchemyError as e:
                logger.error(f"Error saving search result: {e}")
                # Continue with the request even if saving the search result fails
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            logger.error(f"Response content: {e.response.text if e.response else 'No response content'}")
            raise HTTPException(status_code=500, detail=f"Error fetching availability data: {str(e)}")

        logger.info("Combining hotel and availability data")
        combined_data = []
        for hotel in hotels:
            if hotel['hotel_id'] not in sandbox_hotel_ids:
                logger.info(f"Skipping hotel {hotel['hotel_id']} as it's not in sandbox_hotel_ids")
                continue

            logger.info(f"Processing hotel: {hotel['hotel_id']} - {hotel['hotel_name']}")
            
            hotel_data = HotelResponse(
                hotel_id=hotel['hotel_id'],
                hotel_name=hotel['hotel_name'],
                star_rating=hotel['star_rating'],
                image_url=hotel.get('image_url'),
                address=hotel.get('address'),
                description=hotel.get('description'),
                cheapest_price=None,
                benefits=[],
                free_cancellation=False,
                free_breakfast=False,
                rooms=[]
            )
            
            live_data = next((prop for prop in availability_data.get("properties", []) if int(prop["propertyId"]) == hotel['hotel_id']), None)
            if live_data:
                logger.info(f"Live data found for hotel {hotel['hotel_id']}")
                rooms = live_data.get("rooms", [])
                hotel_data.rooms = [
                    Room(roomId=room["roomId"], roomName=room["roomName"], price=room["totalPayment"]["inclusive"])
                    for room in rooms
                ]
                if rooms:
                    hotel_data.cheapest_price = min(room["totalPayment"]["inclusive"] for room in rooms)
                    hotel_data.benefits = list(set(benefit["translatedBenefitName"] for room in rooms for benefit in room.get("benefits", [])))
                    hotel_data.free_cancellation = any(room.get("freeCancellation", False) for room in rooms)
                    hotel_data.free_breakfast = any(room.get("freeBreakfast", False) for room in rooms)
            else:
                logger.warning(f"No live data found for hotel {hotel['hotel_id']}")
            
            combined_data.append(hotel_data)

        logger.info(f"Returning {len(combined_data)} hotels with availability data")
        return HotelListResponse(hotels=combined_data)
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")