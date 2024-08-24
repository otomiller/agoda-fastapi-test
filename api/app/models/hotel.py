from sqlalchemy import Column, Integer, String, Float
from app.core.database_config import Base

class Hotel(Base):
    __tablename__ = "hotels"

    # Update these fields to match your actual database structure
    hotel_id = Column(Integer, primary_key=True, index=True)
    hotel_name = Column(String, index=True)
    star_rating = Column(Float)
    city_id = Column(Integer, index=True)
    # Add any other fields that are in your hotels table