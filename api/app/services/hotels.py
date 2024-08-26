import httpx
from fastapi import HTTPException
import xml.etree.ElementTree as ET
import logging
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.hotel import Hotel, HotelDescription, Address, Picture
from typing import List, Dict
from sqlalchemy.orm import selectinload


logger = logging.getLogger(__name__)

async def fetch_hotel_list(city_id: int):
    url = f"https://affiliatefeed.agoda.com/datafeeds/feed/getfeed?apikey={settings.API_KEY}&mtypeid=3&feed_id=5&mCity_id={city_id}"
    
    async with httpx.AsyncClient() as client:
        logger.info(f"Fetching hotel list for city ID: {city_id}")
        response = await client.get(url)
        response.raise_for_status()
        
        root = ET.fromstring(response.text)
        hotels = []
        for hotel in root.findall(".//hotel"):
            hotels.append({
                "hotel_id": int(hotel.find("hotel_id").text),
                "hotel_name": hotel.find("hotel_name").text,
                "star_rating": float(hotel.find("star_rating").text) if hotel.find("star_rating").text else 0.0,
                # Add other fields as needed
            })
        
        logger.info(f"Found {len(hotels)} hotels for city ID: {city_id}")
        return hotels

async def get_hotels_from_db(db: AsyncSession, city_id: int) -> List[Dict]:
    query = select(
        Hotel.hotel_id,
        Hotel.hotel_name,
        Hotel.star_rating.cast(Float),  # Cast to Float
        func.coalesce(
            select(Picture.url)
            .where((Picture.hotel_id == Hotel.hotel_id) & (Picture.caption == 'Exterior view'))
            .limit(1)
            .scalar_subquery(),
            ''
        ).label('image_url'),
        func.coalesce(
            select(Address.address_line_1)
            .where(Address.hotel_id == Hotel.hotel_id)
            .limit(1)
            .scalar_subquery(),
            ''
        ).label('address'),
        func.coalesce(
            select(HotelDescription.description_text)
            .where(HotelDescription.hotel_id == Hotel.hotel_id)
            .limit(1)
            .scalar_subquery(),
            ''
        ).label('description')
    ).where(Hotel.city_id == city_id).limit(20)

    result = await db.execute(query)
    return [dict(row) for row in result.fetchall()]

async def fetch_hotel_detail(hotel_id: int, db: AsyncSession):
    try:
        # Use selectinload to eagerly load relationships
        result = await db.execute(
            select(Hotel)
            .options(selectinload(Hotel.addresses), selectinload(Hotel.description))
            .where(Hotel.hotel_id == hotel_id)
        )
        hotel = result.scalar_one_or_none()

        if not hotel:
            logger.warning(f"Hotel with ID {hotel_id} not found.")
            raise HTTPException(status_code=404, detail=f"Hotel not found with ID: {hotel_id}")

        # Fetch the address and description
        if hotel.addresses:
            address = hotel.addresses[0]  # Select the first address for simplicity (or adjust as needed)
            address_str = f"{address.street}, {address.city}, {address.country}"  # Adjust based on your Address model
        else:
            address_str = "Address not available"

        hotel_data = {
            'hotel_id': hotel.hotel_id,
            'hotel_name': hotel.hotel_name,
            'star_rating': hotel.star_rating,
            'address': address_str,
            'description': hotel.description.description_text if hotel.description else "Description not available",
            'amenities': [],  # Update this part with amenities if available in related models
        }

        return hotel_data

    except HTTPException as http_ex:
        logger.error(f"HTTPException: {http_ex.detail}")
        raise
    except Exception as e:
        # Log the full exception details for troubleshooting
        logger.error(f"Error fetching hotel detail for hotel ID {hotel_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching hotel detail.")    