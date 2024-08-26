from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.hotel import Hotel, HotelDescription, Address, Picture, SearchResult
from typing import List, Dict
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

# async def save_search_result(db: AsyncSession, search_id: str | int, response_data: dict):
#     """
#     Save the search result to the database.
#     """
#     search_result = SearchResult(
#         search_id=str(search_id),  # Convert to string
#         response_data=json.dumps(response_data)
#     )
#     db.add(search_result)
#     await db.commit()

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