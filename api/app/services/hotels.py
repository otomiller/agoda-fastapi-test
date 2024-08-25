import httpx
import xml.etree.ElementTree as ET
import logging
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.hotel import Hotel, HotelDescription, Address, Picture
from typing import List, Dict

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
        Hotel.star_rating,
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
            select(HotelDescription.overview)
            .where(HotelDescription.hotel_id == Hotel.hotel_id)
            .limit(1)
            .scalar_subquery(),
            ''
        ).label('description')
    ).where(Hotel.city_id == city_id).limit(20)

    result = await db.execute(query)
    return [dict(row) for row in result.fetchall()]

# Add other functions like get_hotel_detail here if needed