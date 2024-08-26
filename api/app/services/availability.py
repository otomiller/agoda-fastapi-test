import asyncio
import httpx
import logging
from app.core.config import settings
from app.schemas.hotel import RoomRequest

logger = logging.getLogger(__name__)

# Hardcoded list of hotel IDs for sandbox mode
sandbox_hotel_ids = [
    28722004, 28721997, 28722003, 28722002, 28722001, 28722000, 28721999, 
    28721998, 28722006, 28722005, 2937, 64748, 105040, 105262, 147265, 
    1144272, 1144275, 2064981, 6139, 70299, 61912, 782709, 9107, 90772, 
    263253, 178562, 51461, 285764, 51921, 267656, 178523, 6063, 240568, 
    234458, 267698, 196931, 267121, 240353, 42976, 6852414, 9412311, 
    1095091, 1193699, 4521, 118508, 11484, 2713, 43775, 70697, 178188, 
    7947, 4877
]

async def fetch_availability_for_sandbox(room_request: RoomRequest):
    """
    Fetch availability for the hardcoded sandbox hotel IDs.
    """
    logger.info(f"Fetching availability for sandbox hotels with {len(sandbox_hotel_ids)} properties")

    async with httpx.AsyncClient(timeout=10.0) as client:
        payload = {
            "waitTime": 60,
            "criteria": {
                "propertyIds": sandbox_hotel_ids,  # Hardcoded sandbox hotel IDs
                "checkIn": room_request.checkIn,
                "checkOut": room_request.checkOut,
                "rooms": room_request.rooms,
                "adults": room_request.adults,
                "children": room_request.children,
                "childrenAges": [5, 6],  # Static children ages as requested
                "language": "en-us",
                "currency": "USD",
                "userCountry": "US"
            },
            "features": {
                "ratesPerProperty": 1,  # Set the limit to 1 as per the API documentation
                "extra": [
                    "content",
                    "surchargeDetail",
                    "CancellationDetail",
                    "BenefitDetail",
                    "dailyRate",
                    "taxDetail",
                    "rateDetail",
                    "promotionDetail"
                ]
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": settings.AUTHORIZATION,  # Use the settings
        }
        
        url = settings.AVAILABILITY_API_URL
        
        logger.info(f"Request URL: {url}")
        logger.info(f"Request Headers: {headers}")
        logger.info(f"Request Payload: {payload}")
        
        try:
            response = await client.post(url, headers=headers, json=payload)
            logger.info(f"Response Status Code: {response.status_code}")
            logger.info(f"Response Headers: {response.headers}")
            logger.info(f"Response Content: {response.text[:1000]}")  # Print first 1000 characters
            
            response.raise_for_status()

            # Log the response for each hotel in the response
            response_data = response.json()
            if "properties" in response_data:
                for property_data in response_data["properties"]:
                    logger.info(f"Hotel ID: {property_data.get('propertyId')} - Name: {property_data.get('propertyName')}")
                    logger.info(f"Rooms: {property_data.get('rooms')}")

            return response.json()

        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            logger.error(f"Response content: {e.response.text if e.response else 'No response content'}")
            return {"error": str(e), "hotel_ids": sandbox_hotel_ids}  # Return the failed hotel IDs
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return {"error": str(e), "hotel_ids": sandbox_hotel_ids}  # Return the failed hotel IDs

async def fetch_availability(room_request: RoomRequest):
    """
    Fetch availability for the sandbox mode only.
    """
    return await fetch_availability_for_sandbox(room_request)

async def fetch_availability_for_hotel(hotel_id: int, search_id: str) -> dict:
    url = f"https://hotelapi.loyalty.dev/api/hotels/{hotel_id}/availability?search_id={search_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()