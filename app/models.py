from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class Hotel(Base):
    __tablename__ = "hotels"

    hotel_id = Column(Integer, primary_key=True, index=True)
    hotel_name = Column(String, nullable=False)
    translated_name = Column(String)
    star_rating = Column(Float)
    longitude = Column(Float)
    latitude = Column(Float)
    remark = Column(String)
    number_of_reviews = Column(Integer)
    rating_average = Column(Float)