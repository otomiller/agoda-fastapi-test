from pydantic import BaseModel
from typing import List, Optional

class HotelBase(BaseModel):
    hotel_name: str
    hotel_formerly_name: Optional[str] = None
    translated_name: Optional[str] = None
    star_rating: Optional[float] = None
    continent_id: Optional[int] = None
    country_id: Optional[int] = None
    city_id: Optional[int] = None
    area_id: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    hotel_url: Optional[str] = None
    popularity_score: Optional[int] = None
    remark: Optional[str] = None
    number_of_reviews: Optional[int] = None
    rating_average: Optional[float] = None
    accommodation_type: Optional[str] = None
    nationality_restrictions: Optional[str] = None
    single_room_property: Optional[bool] = None

class Hotel(HotelBase):
    hotel_id: int

    class Config:
        orm_mode = True

class HotelDescription(BaseModel):
    overview: Optional[str] = None
    snippet: Optional[str] = None

    class Config:
        orm_mode = True

class Facility(BaseModel):
    property_group_description: Optional[str] = None
    property_id: Optional[int] = None
    property_name: Optional[str] = None
    property_translated_name: Optional[str] = None

    class Config:
        orm_mode = True

class RoomTypePicture(BaseModel):
    picture_url: str

    class Config:
        orm_mode = True

class RoomType(BaseModel):
    hotel_room_type_id: int
    standard_caption: Optional[str] = None
    standard_caption_translated: Optional[str] = None
    max_occupancy_per_room: Optional[int] = None
    no_of_room: Optional[int] = None
    size_of_room: Optional[float] = None
    room_size_incl_terrace: Optional[bool] = None
    views: Optional[str] = None
    max_extrabeds: Optional[int] = None
    max_infant_in_room: Optional[int] = None
    hotel_room_type_picture: Optional[str] = None
    bed_type: Optional[str] = None
    hotel_master_room_type_id: Optional[int] = None
    hotel_room_type_alternate_name: Optional[str] = None
    shared_bathroom: Optional[bool] = None
    smoking_nonsmoking: Optional[str] = None
    gender: Optional[str] = None
    pictures: List[RoomTypePicture] = []

    class Config:
        orm_mode = True

class HotelDetail(BaseModel):
    hotel: Hotel
    description: Optional[HotelDescription] = None
    facilities: List[Facility] = []
    rooms: List[RoomType] = []

    class Config:
        orm_mode = True

class AvailabilityRoom(BaseModel):
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
    totalPayment: dict
    roomTypeNotGuaranteed: bool
    paymentModel: str
    rate: dict

class HotelWithAvailability(Hotel):
    rooms: List[AvailabilityRoom] = []

    class Config:
        orm_mode = True