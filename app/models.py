from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Hotel(Base):
    __tablename__ = "hotels"

    hotel_id = Column(Integer, primary_key=True, index=True)
    hotel_name = Column(String, nullable=False)
    hotel_formerly_name = Column(String)
    translated_name = Column(String)
    star_rating = Column(Float)
    continent_id = Column(Integer)
    country_id = Column(Integer, ForeignKey('cities.country_id'))
    city_id = Column(Integer, ForeignKey('cities.city_id'))
    area_id = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
    hotel_url = Column(Text)
    popularity_score = Column(Integer)
    remark = Column(Text)
    number_of_reviews = Column(Integer)
    rating_average = Column(Float)
    accommodation_type = Column(String(50))
    nationality_restrictions = Column(Text)
    single_room_property = Column(Boolean)

    description = relationship("HotelDescription", back_populates="hotel", uselist=False)
    facilities = relationship("Facility", back_populates="hotel")
    room_types = relationship("RoomType", back_populates="hotel")

class HotelDescription(Base):
    __tablename__ = "hotel_descriptions"

    hotel_id = Column(Integer, ForeignKey('hotels.hotel_id'), primary_key=True)
    overview = Column(Text)
    snippet = Column(Text)

    hotel = relationship("Hotel", back_populates="description")

class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey('hotels.hotel_id'))
    property_group_description = Column(String(255))
    property_id = Column(Integer)
    property_name = Column(String(255))
    property_translated_name = Column(String(255))

    hotel = relationship("Hotel", back_populates="facilities")

class RoomType(Base):
    __tablename__ = "room_types"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey('hotels.hotel_id'))
    hotel_room_type_id = Column(Integer)
    standard_caption = Column(Text)
    standard_caption_translated = Column(Text)
    max_occupancy_per_room = Column(Integer)
    no_of_room = Column(Integer)
    size_of_room = Column(Float)
    room_size_incl_terrace = Column(Boolean)
    views = Column(Text)
    max_extrabeds = Column(Integer)
    max_infant_in_room = Column(Integer)
    hotel_room_type_picture = Column(Text)
    bed_type = Column(Text)
    hotel_master_room_type_id = Column(Integer)
    hotel_room_type_alternate_name = Column(Text)
    shared_bathroom = Column(Boolean)
    smoking_nonsmoking = Column(String(50))
    gender = Column(String(50))

    hotel = relationship("Hotel", back_populates="room_types")
    pictures = relationship("RoomTypePicture", back_populates="room_type")

class RoomTypePicture(Base):
    __tablename__ = "room_type_pictures"

    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey('room_types.id'))
    picture_url = Column(Text)

    room_type = relationship("RoomType", back_populates="pictures")