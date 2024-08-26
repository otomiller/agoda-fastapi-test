from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.core.database_config import Base  # Use this as your Base

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

    hotel_id = Column(Integer, ForeignKey("hotels.hotel_id", ondelete="CASCADE"), primary_key=True)
    description_text = Column(Text)

    hotel = relationship("Hotel", back_populates="description")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.hotel_id", ondelete="CASCADE"), nullable=False)
    address_line_1 = Column(String)

    hotel = relationship("Hotel", back_populates="addresses")


class Picture(Base):
    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.hotel_id", ondelete="CASCADE"), nullable=False)
    caption = Column(String)
    url = Column(String)

    hotel = relationship("Hotel", back_populates="pictures")


class SearchResult(Base):
    __tablename__ = "search_results"

    search_id = Column(String, primary_key=True)
    response_data = Column(JSONB)  # Store as JSONB in PostgreSQL