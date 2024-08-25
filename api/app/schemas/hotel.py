from pydantic import BaseModel
from typing import List, Optional

class RoomRequest(BaseModel):
    cityId: int
    checkIn: str
    checkOut: str

class Room(BaseModel):
    roomId: str
    roomName: str
    price: float

class HotelResponse(BaseModel):
    hotel_id: int
    hotel_name: str
    star_rating: int
    rooms: Optional[List[Room]] = None

class HotelListResponse(BaseModel):
    hotels: List[HotelResponse]
    message: Optional[str] = None

class HotelDetailResponse(BaseModel):
    hotel_id: int
    hotel_name: str
    star_rating: int
    address: str
    description: str
    amenities: List[str]
    rooms: List[Room]