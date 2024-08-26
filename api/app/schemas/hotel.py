from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.schemas.room import Room 
from typing import Optional


class HotelBase(BaseModel):
    hotel_id: int
    hotel_name: str
    star_rating: float
    address: str
    image_url: str
    description: str

class Hotel(HotelBase):
    cheapest_price: float
    benefits: List[str]
    free_cancellation: bool
    free_breakfast: bool

class HotelSearch(BaseModel):
    checkIn: str
    checkOut: str
    rooms: int
    adults: int
    children: int
    cityId: int

class RoomType(BaseModel):
    id: int
    hotel_room_type_id: int
    standard_caption: str
    size_of_room: float
    max_occupancy_per_room: int
    room_details: Dict[str, Any]

class HotelDetails(BaseModel):
    hotel_name: str
    address_line_1: str
    longitude: float
    latitude: float
    images: Dict[str, List[str]]
    facilities: List[Dict[str, Any]]
    room_types: List[RoomType]

class HotelResponse(BaseModel):
    hotel_id: int
    hotel_name: str
    star_rating: float
    address: str
    image_url: str
    description: str
    cheapest_price: Optional[float]  # Allow None
    benefits: List[str]
    free_cancellation: bool
    free_breakfast: bool
    rooms: List[Room]
    

class RoomRequest(BaseModel):
    checkIn: str = Field(..., example="2024-11-23")
    checkOut: str = Field(..., example="2024-11-28")
    rooms: int = Field(..., example=1)
    adults: int = Field(..., example=2)
    children: int = Field(..., example=2)
    childrenAges: List[int] = Field(..., example=[5, 6])
    cityId: int = Field(..., example=3987)

# class Room(BaseModel):
#     roomId: int
#     roomName: str
#     price: float
#     currency: str
#     benefits: List[str]

class HotelListResponse(BaseModel):
    hotels: List[HotelResponse]
    message: Optional[str] = None
    search_id: Optional[str] = None


class RoomType(BaseModel):
    id: int
    hotel_room_type_id: int
    standard_caption: str
    size_of_room: Optional[float] = None
    max_occupancy_per_room: int
    room_details: Dict[str, Any]

class HotelDetails(BaseModel):
    hotel_name: str
    address_line_1: str
    longitude: float
    latitude: float
    images: Dict[str, List[str]]
    facilities: List[Dict[str, Any]]
    room_types: List[RoomType]