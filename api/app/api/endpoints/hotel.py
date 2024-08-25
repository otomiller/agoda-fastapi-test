from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import httpx

from app.core.database import get_db
from app.schemas.hotel import HotelDetailResponse
from app.services.hotels import fetch_hotel_detail
from app.services.availability import fetch_availability_for_hotel

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/hotel/{hotel_id}", response_model=HotelDetailResponse)
async def get_hotel_detail(hotel_id: int, search_id: str, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Fetching hotel detail for hotel ID: {hotel_id}")
        hotel = await fetch_hotel_detail(db, hotel_id)

        if not hotel:
            logger.warning(f"No hotel found for the hotel ID: {hotel_id}")
            raise HTTPException(status_code=404, detail=f"Hotel not found with ID: {hotel_id}")

        logger.info(f"Fetching availability for hotel ID: {hotel_id}")
        try:
            availability_data = await fetch_availability_for_hotel(hotel_id, search_id)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning(f"No availability data found for hotel ID: {hotel_id}")
                availability_data = {"rooms": []}
            else:
                logger.error(f"Error fetching availability data: {e}")
                raise HTTPException(status_code=500, detail=f"Error fetching availability data: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching availability data: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error fetching availability data: {str(e)}")

        logger.info("Combining hotel and availability data")
        hotel_detail = HotelDetailResponse(
            hotel_id=hotel['hotel_id'],
            hotel_name=hotel['hotel_name'],
            star_rating=hotel['star_rating'],
            address=hotel.get('address', ''),
            description=hotel.get('description', ''),
            amenities=hotel.get('amenities', []),
            rooms=availability_data.get("rooms", [])
        )

        logger.info(f"Returning hotel detail for hotel ID: {hotel_id}")
        return hotel_detail
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")