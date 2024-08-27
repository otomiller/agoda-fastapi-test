from pydantic import BaseModel
from typing import List, Dict

class RoomRequest(BaseModel):
    cityId: int
    checkInDate: str
    checkOutDate: str
    roomsQuantity: int
    adultsQuantity: int
    childrenQuantity: int

class Room(BaseModel):
    roomId: str
    roomName: str
    price: float
    currency: str = "USD"
    benefits: List[str] = []

class HotelResponse(BaseModel):
    hotel_id: int
    hotel_name: str
    star_rating: float
    image_url: str = None
    address: str = None
    description: str = None
    cheapest_price: float = None
    benefits: List[str] = []
    free_cancellation: bool = False
    free_breakfast: bool = False
    rooms: List[Room]

class HotelListResponse(BaseModel):
    hotels: List[HotelResponse]
    search_id: str

class RoomType(BaseModel):
    id: str
    hotel_room_type_id: str
    standard_caption: str
    size_of_room: str = None
    max_occupancy_per_room: int
    room_details: dict

class HotelDetails(BaseModel):
    hotel_name: str
    address_line_1: str
    longitude: float
    latitude: float
    images: Dict[str, List[str]]
    facilities: List[str]
    room_types: List[RoomType]
    room_types_data: List[dict]  # Add this line to include the query result