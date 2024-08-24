import httpx
from app.core.config import settings
from app.schemas.hotel import RoomRequest

async def fetch_availability(room_request: RoomRequest):
    async with httpx.AsyncClient() as client:
        params = {
            "apikey": settings.API_KEY,
            "checkIn": room_request.checkIn,
            "checkOut": room_request.checkOut,
            "rooms": room_request.rooms,
            "adults": room_request.adults,
            "children": room_request.children,
            "cityId": room_request.cityId,
            "siteID": 1923846,
        }
        response = await client.get(settings.AVAILABILITY_API_URL, params=params)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()