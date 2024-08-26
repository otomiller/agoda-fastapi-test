from sqlalchemy.orm import Session
from sqlalchemy import text

async def fetch_hotel_basic_info(db: Session, hotel_id: int):
    query = text("""
    WITH hotel_details AS (
        SELECT 
            h.hotel_name,
            a.address_line_1,
            h.longitude, 
            h.latitude
        FROM 
            public.hotels h
        JOIN 
            public.addresses a ON h.hotel_id = a.hotel_id
        WHERE 
            h.hotel_id = :hotel_id
        LIMIT 1
    ),
    grouped_pictures AS (
        SELECT 
            json_object_agg(caption, urls) AS images
        FROM (
            SELECT 
                caption, 
                json_agg(url) AS urls
            FROM 
                public.pictures
            WHERE 
                hotel_id = :hotel_id
            GROUP BY 
                caption
        ) AS subquery
    ),
    grouped_facilities AS (
        SELECT 
            json_agg(
                json_build_object(
                    'property_group_description', property_group_description,
                    'facilities', facilities
                )
            ) AS grouped_facilities
        FROM (
            SELECT 
                property_group_description, 
                array_agg(property_name) AS facilities
            FROM 
                public.facilities
            WHERE 
                hotel_id = :hotel_id
            GROUP BY 
                property_group_description
        ) subquery
    )

    SELECT json_build_object(
        'hotel_name', hd.hotel_name,
        'address_line_1', hd.address_line_1,
        'longitude', hd.longitude,
        'latitude', hd.latitude,
        'images', gp.images,
        'facilities', gf.grouped_facilities
    ) AS hotel_data
    FROM 
        hotel_details hd,
        grouped_pictures gp,
        grouped_facilities gf;
    """)
    result = await db.execute(query, {'hotel_id': hotel_id})
    return result.scalar_one()

async def fetch_availability_data(db: Session, search_id: str, hotel_id: int):
    query = text("""
    SELECT response_data->'properties' as properties
    FROM search_results
    WHERE search_id = :search_id;
    """)
    result = await db.execute(query, {'search_id': search_id})
    properties = result.scalar_one()
    
    for property in properties:
        if property['propertyId'] == hotel_id:
            return property
    
    raise ValueError("Hotel not found in search results")

async def fetch_room_types(db: Session, hotel_id: int, room_ids: list):
    query = text("""
    SELECT json_agg(row_to_json(rt))
    FROM (
        SELECT * 
        FROM public.room_types 
        WHERE hotel_id = :hotel_id 
        AND hotel_room_type_id = ANY(:room_ids)
    ) rt;
    """)
    result = await db.execute(query, {'hotel_id': hotel_id, 'room_ids': room_ids})
    return result.scalar_one()