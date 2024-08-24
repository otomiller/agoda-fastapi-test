import httpx
from app.core.config import settings
from app.schemas.hotel import RoomRequest

async def fetch_availability(room_request: RoomRequest):
    async with httpx.AsyncClient() as client:
        params = {
            "apikey": settings.API_KEY,
            "mdate": room_request.checkIn,
            "mtypeid": 1,
            "siteID": 1923846,
            # Add other necessary parameters
        }
        response = await client.get(settings.AVAILABILITY_API_URL, params=params)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()