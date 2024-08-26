from pydantic import BaseModel
from typing import List, Optional

class RoomRequest(BaseModel):
    checkIn: str
    checkOut: str
    rooms: int
    adults: int
    children: int
    cityId: int

class Room(BaseModel):
    roomId: int
    roomName: str
    price: float

class HotelResponse(BaseModel):
    hotel_id: int
    hotel_name: str
    star_rating: float
    image_url: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    cheapest_price: Optional[float] = None
    benefits: Optional[List[str]] = None
    free_cancellation: Optional[bool] = None
    free_breakfast: Optional[bool] = None
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