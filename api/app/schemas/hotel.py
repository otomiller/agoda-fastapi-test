from pydantic import BaseModel
from typing import List, Dict, Any, Optional


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

class HotelDetailResponse(BaseModel):
    hotel_id: int
    hotel_name: str
    star_rating: int
    address: str
    description: str
    amenities: List[str]
    rooms: List[Room]
    
# Add the missing schemas
class RoomRequest(BaseModel):
    checkIn: str
    checkOut: str
    rooms: int
    adults: int
    children: int
    childrenAges: List[int]
    cityId: int

class Room(BaseModel):
    roomId: int
    roomName: str
    price: float
    currency: str
    benefits: List[str]

class HotelListResponse(BaseModel):
    hotels: List[Hotel]
    rooms: List[Room]

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