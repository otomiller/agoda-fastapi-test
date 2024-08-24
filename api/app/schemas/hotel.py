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
    roomId: str
    roomName: str
    price: float

class HotelResponse(BaseModel):
    hotel_id: int
    hotel_name: str
    star_rating: float
    rooms: Optional[List[Room]] = None