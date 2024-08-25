import httpx
import xml.etree.ElementTree as ET
import logging
from app.core.config import settings

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