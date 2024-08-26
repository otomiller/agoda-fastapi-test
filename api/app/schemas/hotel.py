from typing import List, Optional
from pydantic import BaseModel

class RoomRequest(BaseModel):
    city_id: int
    checkin: str
    checkout: str
    rooms: int
    adults: int
    children: int
    cid: Optional[int] = None
    search_id: Optional[str] = None

class Room(BaseModel):
    room_id: int
    room_name: str
    price: float
    currency: str

class HotelResponse(BaseModel):
    hotel_id: int
    hotel_name: str
    star_rating: float
    address: str
    image_url: str
    description: str

class HotelListResponse(BaseModel):
    hotels: List[HotelResponse]

class HotelDetailResponse(BaseModel):
    hotel_id: int
    hotel_name: str
    star_rating: float
    address: str
    description: str
    amenities: List[str]
    rooms: List[Room]