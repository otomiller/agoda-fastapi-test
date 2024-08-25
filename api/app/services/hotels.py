from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.hotel import Hotel
import logging

logger = logging.getLogger(__name__)

async def fetch_hotel_list(city_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Hotel).where(Hotel.city_id == city_id))
        hotels = result.scalars().all()
        return [
            {
                'hotel_id': hotel.hotel_id,
                'hotel_name': hotel.hotel_name,
                'star_rating': hotel.star_rating,
            }
            for hotel in hotels
        ]
    except Exception as e:
        logger.error(f"Error fetching hotel list: {e}")
        raise

async def fetch_hotel_detail(hotel_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Hotel).where(Hotel.hotel_id == hotel_id))
        hotel = result.scalar_one_or_none()
        if hotel:
            return {
                'hotel_id': hotel.hotel_id,
                'hotel_name': hotel.hotel_name,
                'star_rating': hotel.star_rating,
                'address': hotel.address,
                'description': hotel.description,
                'amenities': hotel.amenities,
            }
        return None
    except Exception as e:
        logger.error(f"Error fetching hotel detail: {e}")
        raise