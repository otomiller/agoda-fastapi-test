from fastapi import FastAPI, HTTPException
from db.db_connect import get_db_connection
from pydantic import BaseModel

app = FastAPI()

class AvailabilityRequest(BaseModel):
    checkIn: str
    checkOut: str
    rooms: int
    adults: int
    children: int
    hotelId: int

class MultiHotelAvailabilityRequest(BaseModel):
    checkIn: str
    checkOut: str
    rooms: int
    adults: int
    children: int
    hotelId: list[int]

@app.get("/hotel/list")
def get_hotels_by_city(city_id: int):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        query = "SELECT hotel_id, hotel_name FROM hotels WHERE city_id = %s"
        cursor.execute(query, (city_id,))
        hotels = cursor.fetchall()
    return {"hotels": hotels}

@app.get("/hotel/details/{hotel_id}")
def get_hotel_details(hotel_id: int):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        query = "SELECT * FROM hotels WHERE hotel_id = %s"
        cursor.execute(query, (hotel_id,))
        hotel = cursor.fetchone()
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")
    return {"hotel": hotel}

@app.get("/hotel/detailed_page/{hotel_id}")
def get_hotel_detailed_page(hotel_id: int):
    connection = get_db_connection()
    data = {}

    with connection.cursor() as cursor:
        # Get hotel details
        hotel_query = "SELECT * FROM hotels WHERE hotel_id = %s"
        cursor.execute(hotel_query, (hotel_id,))
        data["hotel"] = cursor.fetchone()

        # Get hotel descriptions
        description_query = "SELECT * FROM hotel_descriptions WHERE hotel_id = %s"
        cursor.execute(description_query, (hotel_id,))
        data["descriptions"] = cursor.fetchall()

        # Get hotel facilities
        facilities_query = "SELECT * FROM facilities WHERE hotel_id = %s"
        cursor.execute(facilities_query, (hotel_id,))
        data["facilities"] = cursor.fetchall()

        # Get room types
        room_query = "SELECT * FROM room_types WHERE hotel_id = %s"
        cursor.execute(room_query, (hotel_id,))
        data["rooms"] = cursor.fetchall()

    return data

@app.post("/hotel/specific_availability")
def check_hotel_availability(data: AvailabilityRequest):
    # Simulate API interaction for hotel availability
    availability_response = {
        "hotel_id": data.hotelId,
        "availability_status": "Available",
        "price_per_night": 150.00
    }
    return availability_response

@app.post("/hotel/specific_availability/multi")
def check_multi_hotel_availability(data: MultiHotelAvailabilityRequest):
    # Simulate API interaction for multiple hotels
    availability_results = []
    for hotel_id in data.hotelId:
        availability_response = {
            "hotel_id": hotel_id,
            "availability_status": "Available",
            "price_per_night": 150.00
        }
        availability_results.append(availability_response)
    
    return availability_results