# import httpx
# from app.core.config import settings
# from app.schemas.hotel import RoomRequest

# async def fetch_availability(room_request: RoomRequest):
#     async with httpx.AsyncClient() as client:
#         params = {
#             "apikey": settings.API_KEY,
#             "checkIn": room_request.checkIn,
#             "checkOut": room_request.checkOut,
#             "rooms": room_request.rooms,
#             "adults": room_request.adults,
#             "children": room_request.children,
#             "cityId": room_request.cityId,
#             "siteID": 1923846,
#         }
#         try:
#             response = await client.post(settings.AVAILABILITY_API_URL, json=params)
#             response.raise_for_status()  # This will raise an exception for HTTP errors
#             return response.json()
#         except httpx.HTTPError as e:
#             print(f"HTTP Exception for {e.request.url} - {e}")
#             return {"properties": []}  # Return an empty list of properties on error
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return {"properties": []}  # Return an empty list of properties on error
import httpx
import json
import logging
from app.core.config import settings
from app.schemas.hotel import RoomRequest

logger = logging.getLogger(__name__)

async def fetch_availability(room_request: RoomRequest, property_ids: list[int]):
    logger.info(f"Fetching availability for {len(property_ids)} properties")
    
    # Prepare the request payload
    payload = {
        "waitTime": 60,
        "criteria": {
            "propertyIds": property_ids,
            "checkIn": room_request.checkIn,
            "checkOut": room_request.checkOut,
            "rooms": room_request.rooms,
            "adults": room_request.adults,
            "children": room_request.children,
            "childrenAges": [5, 6],  # Adjust this dynamically
            "language": "en-us",
            "currency": "USD",
            "userCountry": "US"
        },
        "features": {
            "ratesPerProperty": 25,
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
    
    # Set the headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": settings.AUTHORIZATION,  # Correctly use the settings
    }
    
    # API URL
    url = settings.AVAILABILITY_API_URL
    
    logger.info(f"Request URL: {url}")
    logger.info(f"Request Headers: {json.dumps(headers, indent=2)}")
    logger.info(f"Request Payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Define the client inside the try block
        async with httpx.AsyncClient() as client:
            # Send the request
            response = await client.post(url, headers=headers, json=payload)
            logger.info(f"Response Status Code: {response.status_code}")
            logger.info(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
            logger.info(f"Response Content: {response.text[:1000]}...")  # Print first 1000 characters
            
            # Check if the request was successful
            response.raise_for_status()
            return response.json()
    
    except httpx.HTTPError as e:
        # Log the HTTP error
        logger.error(f"HTTP error occurred: {e}")
        logger.error(f"Response content: {e.response.text if e.response else 'No response content'}")
        raise
    
    except Exception as e:
        # Log any unexpected errors
        logger.error(f"Unexpected error occurred: {e}")
        raise