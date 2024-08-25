from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database_config import Base

class Hotel(Base):
    __tablename__ = "hotels"

    hotel_id = Column(Integer, primary_key=True, index=True)
    hotel_name = Column(String, index=True)
    star_rating = Column(Float)
    city_id = Column(Integer, index=True)
    longitude = Column(Float)
    latitude = Column(Float)

    description = relationship("HotelDescription", back_populates="hotel", uselist=False)
    addresses = relationship("Address", back_populates="hotel")
    pictures = relationship("Picture", back_populates="hotel")

class HotelDescription(Base):
    __tablename__ = "hotel_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.hotel_id"))
    overview = Column(Text)

    hotel = relationship("Hotel", back_populates="description")

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.hotel_id"))
    address_line_1 = Column(String)

    hotel = relationship("Hotel", back_populates="addresses")

class Picture(Base):
    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.hotel_id"))
    caption = Column(String)
    url = Column(String)

    hotel = relationship("Hotel", back_populates="pictures")

class SearchResult(Base):
    __tablename__ = "search_results"

    search_id = Column(String, primary_key=True)
    response_data = Column(JSON)