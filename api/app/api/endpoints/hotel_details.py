from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.hotel import HotelDetailResponse, RoomTypeDetail
from app.services.hotels import get_hotel_detail
from app.services.availability import fetch_availability
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/hotel/{hotel_id}", response_model=HotelDetailResponse)
async def get_hotel_details(hotel_id: int, search_id: str, db: AsyncSession = Depends(get_db)):
    try:
        hotel_data = await get_hotel_detail(db, hotel_id)
        
        if not hotel_data:
            raise HTTPException(status_code=404, detail="Hotel not found")

        # Fetch availability data using the search_id
        # This part needs to be implemented based on how you store and retrieve search results
        availability_data = await fetch_availability_by_search_id(search_id, hotel_id)

        # Combine room types with availability data
        room_types = []
        for room_type in hotel_data['room_types']:
            room_details = next((room for room in availability_data.get('rooms', []) if room['roomId'] == room_type['hotel_room_type_id']), None)
            if room_details:
                room_types.append(RoomTypeDetail(
                    id=room_type['id'],
                    hotel_room_type_id=room_type['hotel_room_type_id'],
                    standard_caption=room_type['standard_caption'],
                    size_of_room=room_type['size_of_room'],
                    max_occupancy_per_room=room_type['max_occupancy_per_room'],
                    room_details=room_details
                ))

        return HotelDetailResponse(
            hotel_name=hotel_data['hotel_name'],
            address_line_1=hotel_data['address_line_1'],
            longitude=hotel_data['longitude'],
            latitude=hotel_data['latitude'],
            images=hotel_data['images'],
            facilities=hotel_data['facilities'],
            room_types=room_types
        )
    except Exception as e:
        logger.error(f"Error fetching hotel details: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching hotel details: {str(e)}")