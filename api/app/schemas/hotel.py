from pydantic import BaseModel
from typing import List, Optional, Dict, Union
from pydantic import BaseModel

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

class Image(BaseModel):
    url: str

class ImageCategory(BaseModel):
    __root__: Dict[str, List[str]]

class Facility(BaseModel):
    property_group_description: str
    facilities: List[str]

class RoomDetail(BaseModel):
    roomId: int
    blockId: str
    roomName: str
    parentRoomName: str
    translatedRoomName: str
    blockIdBackup: str
    parentRoomId: int
    ratePlanId: int
    freeWifi: bool
    remainingRooms: int
    normalBedding: int
    extraBeds: int
    freeBreakfast: bool
    freeCancellation: bool
    totalPayment: Dict[str, float]
    roomTypeNotGuaranteed: bool
    paymentModel: str
    rate: Dict[str, Union[str, float]]
    dailyRate: List[Dict[str, Union[str, float]]]
    promotionDetail: Dict[str, Union[int, bool, str, float]]
    surcharges: List[Dict[str, Union[int, str, Dict[str, Union[str, float]]]]]
    taxBreakdown: List[Dict[str, Union[str, float]]]
    cancellationPolicy: Dict[str, Union[str, List[Dict[str, Union[int, str, float]]]]]
    benefits: List[Dict[str, Union[int, str]]]

class RoomType(BaseModel):
    id: int
    hotel_room_type_id: int
    standard_caption: str
    size_of_room: float
    max_occupancy_per_room: int
    room_details: RoomDetail

class HotelDetailResponse(BaseModel):
    hotel_name: str
    address_line_1: str
    longitude: float
    latitude: float
    images: ImageCategory
    facilities: List[Facility]
    room_types: List[RoomType]