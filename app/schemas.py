from pydantic import BaseModel

class HotelBase(BaseModel):
    hotel_name: str
    translated_name: str = None
    star_rating: float = None
    longitude: float = None
    latitude: float = None
    remark: str = None
    number_of_reviews: int = None
    rating_average: float = None

class Hotel(HotelBase):
    hotel_id: int

    class Config:
        orm_mode = True