from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.schemas.hotel import HotelDetails, RoomType
from app.models.hotel import Hotel, Address, Picture, SearchResult
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from sqlalchemy import text
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.schemas.hotel import HotelDetails, RoomType
from app.models.hotel import Hotel, Address, Picture, SearchResult
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

async def get_hotel_details(db: AsyncSession, hotel_id: int, search_id: str) -> HotelDetails:
    try:
        # Fetch hotel basic info with address and pictures in a single query
        result = await db.execute(
            select(Hotel).options(joinedload(Hotel.addresses), joinedload(Hotel.pictures))
            .filter(Hotel.hotel_id == hotel_id)
        )
        hotel = result.unique().scalar_one()

        if not hotel:
            raise NoResultFound("Hotel not found")

        if not hotel.addresses:
            raise NoResultFound("No address found for this hotel")

        address = hotel.addresses[0]  # Assuming the first address is the main one

        # Process pictures
        images = {}
        for pic in hotel.pictures:
            caption = pic.caption or "Uncategorized"  # Use "Uncategorized" if caption is None
            if caption not in images:
                images[caption] = []
            images[caption].append(pic.url)

        # Fetch availability data
        result = await db.execute(select(SearchResult).filter(SearchResult.search_id == search_id))
        search_result = result.scalar_one()

        # Extract room types from search_result
        properties = search_result.response_data.get('properties', [])
        hotel_data = next((prop for prop in properties if prop['propertyId'] == hotel_id), None)
        
        if not hotel_data:
            raise ValueError("Hotel not found in search results")

        room_types = [
            RoomType(
                id=room['roomId'],
                hotel_room_type_id=room['roomId'],
                standard_caption=room['roomName'],
                size_of_room=None,  # This information might not be available in the search results
                max_occupancy_per_room=room.get('normalBedding', 0),
                room_details=room
            )
            for room in hotel_data.get('rooms', [])
        ]

        # Execute the custom SQL query
        query = text("""
            SELECT * 
            FROM public.room_types 
            WHERE hotel_id = :hotel_id 
            AND hotel_room_type_id = ANY(:room_ids)
        """)
        room_ids = [room['roomId'] for room in hotel_data.get('rooms', [])]
        result = await db.execute(query, {"hotel_id": hotel_id, "room_ids": room_ids})
        room_types_data = [dict(row) for row in result]

        hotel_details = HotelDetails(
            hotel_name=hotel.hotel_name,
            address_line_1=address.address_line_1,
            longitude=hotel.longitude,
            latitude=hotel.latitude,
            images=images,
            facilities=[],  # You might want to fetch facilities separately
            room_types=room_types,
            room_types_data=room_types_data  # Add the query result to the response
        )

        return hotel_details

    except NoResultFound as e:
        raise ValueError(f"No data found: {str(e)}")
    except MultipleResultsFound as e:
        raise ValueError(f"Multiple results found: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error fetching hotel details: {str(e)}")