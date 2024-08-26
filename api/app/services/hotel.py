from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.hotel import Hotel, HotelDescription, Address, Picture, SearchResult
from typing import List, Dict, Optional
import logging
import json

async def get_hotels_from_db(db: AsyncSession, city_id: int) -> List[Dict]:
    query = select(
        Hotel.hotel_id,
        Hotel.hotel_name,
        Hotel.star_rating,
        func.coalesce(
            select(Picture.url)
            .where((Picture.hotel_id == Hotel.hotel_id) & (Picture.caption == 'Exterior view'))
            .limit(1)
            .scalar_subquery(),
            ''
        ).label('image_url'),
        func.coalesce(
            select(Address.address_line_1)
            .where(Address.hotel_id == Hotel.hotel_id)
            .limit(1)
            .scalar_subquery(),
            ''
        ).label('address'),
        func.coalesce(
            select(HotelDescription.overview)
            .where(HotelDescription.hotel_id == Hotel.hotel_id)
            .limit(1)
            .scalar_subquery(),
            ''
        ).label('description')
    ).where(Hotel.city_id == city_id).limit(20)

    result = await db.execute(query)
    return [dict(row) for row in result.fetchall()]

async def get_hotel_detail(db: AsyncSession, hotel_id: int) -> Optional[Dict]:
    query = select(
        Hotel,
        HotelDescription.overview,
        func.coalesce(
            select(Address.address_line_1)
            .where(Address.hotel_id == Hotel.hotel_id)
            .limit(1)
            .scalar_subquery(),
            ''
        ).label('address')
    ).outerjoin(HotelDescription, Hotel.hotel_id == HotelDescription.hotel_id)\
     .where(Hotel.hotel_id == hotel_id)

    result = await db.execute(query)
    row = result.first()

    if not row:
        return None

    hotel, overview, address = row

    # Fetch images
    images_query = select(Picture.caption, Picture.url).where(Picture.hotel_id == hotel_id)
    images_result = await db.execute(images_query)
    images = {}
    for image_row in images_result:
        caption, url = image_row
        if caption not in images:
            images[caption] = []
        images[caption].append(url)

    # Fetch facilities (you might need to adjust this based on your actual data model)
    # If you don't have a Facility model, you can remove or modify this part
    # facilities_query = select(Facility.property_group_description, Facility.property_name)\
    #     .where(Facility.hotel_id == hotel_id)
    # facilities_result = await db.execute(facilities_query)
    # facilities = {}
    # for facility_row in facilities_result:
    #     group, name = facility_row
    #     if group not in facilities:
    #         facilities[group] = []
    #     facilities[group].append(name)

    return {
        "hotel_name": hotel.hotel_name,
        "address_line_1": address,
        "longitude": hotel.longitude,
        "latitude": hotel.latitude,
        "images": images,
        # "facilities": [{"property_group_description": k, "facilities": v} for k, v in facilities.items()],
        "description": overview
    }

async def save_search_result(db: AsyncSession, search_id: str | int, response_data: dict):
    """
    Save the search result to the database.
    """
    search_result = SearchResult(
        search_id=str(search_id),  # Convert to string if necessary
        response_data=response_data  # Pass the dictionary directly to store it as JSONB
    )
    db.add(search_result)
    await db.commit()