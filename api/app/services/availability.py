import httpx
from app.schemas.hotel import RoomRequest

async def fetch_availability(room_request: RoomRequest) -> dict:
    url = "https://hotelapi.loyalty.dev/api/hotels/availability"
    params = {
        "cityId": room_request.cityId,
        "checkIn": room_request.checkIn,
        "checkOut": room_request.checkOut,
        "lang": "en",
        "currency": "USD",
        "countryCode": "US",
        "guests": [{"adults": 2, "children": 0}]
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

async def fetch_availability_for_hotel(hotel_id: int, search_id: str) -> dict:
    url = f"https://hotelapi.loyalty.dev/api/hotels/{hotel_id}/availability?search_id={search_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()