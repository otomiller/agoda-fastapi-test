from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.core.database import get_db
from app.schemas.hotel import HotelDetailResponse
from app.services.hotels import fetch_hotel_detail
from app.services.availability import fetch_availability_for_hotel

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/hotel/{hotel_id}", response_model=HotelDetailResponse)
async def get_hotel_detail(hotel_id: int, search_id: str, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Received request for hotel details. hotel_id: {hotel_id}, search_id: {search_id}")

        # Fetch the hotel details
        hotel = await fetch_hotel_detail(hotel_id)
        if not hotel:
            logger.warning(f"Hotel with ID {hotel_id} not found.")
            raise HTTPException(status_code=404, detail=f"Hotel not found with ID: {hotel_id}")

        logger.info(f"Successfully fetched hotel details for hotel ID: {hotel_id}")

        # Fetch availability data for the hotel
        try:
            logger.info(f"Fetching availability for hotel ID: {hotel_id} and search ID: {search_id}")
            availability_data = await fetch_availability_for_hotel(hotel_id, search_id)
            logger.info(f"Successfully fetched availability for hotel ID: {hotel_id}")
        except Exception as e:
            logger.error(f"Error fetching availability data for hotel ID: {hotel_id}. Error: {e}")
            raise HTTPException(status_code=500, detail=f"Error fetching availability data: {str(e)}")

        # Combine hotel details with availability data
        logger.info(f"Combining hotel details with availability data for hotel ID: {hotel_id}")
        hotel_detail = HotelDetailResponse(
            hotel_id=hotel['hotel_id'],
            hotel_name=hotel['hotel_name'],
            star_rating=hotel['star_rating'],
            address=hotel['address'],
            description=hotel['description'],
            amenities=hotel['amenities'],
            rooms=availability_data.get("rooms", [])
        )

        logger.info(f"Returning hotel details response for hotel ID: {hotel_id}")
        return hotel_detail

    except HTTPException as http_ex:
        logger.error(f"HTTPException: {http_ex.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")