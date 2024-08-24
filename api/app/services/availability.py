import httpx
from app.core.config import settings
from app.schemas.hotel import RoomRequest

async def fetch_availability(room_request: RoomRequest):
    client = httpx.AsyncClient(http2=True)
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
    try:
        response = await client.get(settings.AVAILABILITY_API_URL, params=params)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()
    except httpx.HTTPError as e:
        print(f"HTTP Exception for {e.request.url} - {e}")
        return {"properties": []}  # Return an empty list of properties on error
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"properties": []}  # Return an empty list of properties on error
    finally:
        await client.aclose()