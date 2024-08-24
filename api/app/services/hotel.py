from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.hotel import Hotel, HotelDescription
from app.schemas.hotel import RoomRequest, HotelResponse
from app.services.availability import fetch_availability
from app.services.cache import get_cached_data, set_cached_data

async def get_hotels(db: Session, room_request: RoomRequest):
    cache_key = f"hotels:{room_request.cityId}:{room_request.checkIn}:{room_request.checkOut}"
    
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data
    
    availability_data = await fetch_availability(room_request)
    
    hotels = db.execute(
        select(Hotel).where(Hotel.city_id == room_request.cityId)
    ).scalars().all()
    
    combined_data = []
    for hotel in hotels:
        hotel_data = HotelResponse(
            id=hotel.id,
            name=hotel.name,
            starRating=hotel.star_rating,
            description=hotel.description.overview if hotel.description else "",
        )
        
        live_data = next((prop for prop in availability_data["properties"] if prop["propertyId"] == hotel.id), None)
        if live_data:
            hotel_data.rooms = [
                {"roomId": room["roomId"], "roomName": room["roomName"], "price": room["totalPayment"]["inclusive"]}
                for room in live_data["rooms"]
            ]
        
        combined_data.append(hotel_data.dict())
    
    set_cached_data(cache_key, combined_data)
    
    return combined_data