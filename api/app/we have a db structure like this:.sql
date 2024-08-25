we have a db structure like this:

-- Languages table
CREATE TABLE languages (
    language_id INT PRIMARY KEY,
    language_name VARCHAR(50) NOT NULL,
    translated_name VARCHAR(50) NOT NULL
);

-- Cities table
CREATE TABLE cities (
    city_id INT PRIMARY KEY,
    country_id INT NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    city_translated VARCHAR(100) NOT NULL,
    active_hotels INT NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    latitude DECIMAL(8,6) NOT NULL,
    no_area INT NOT NULL
);

-- Hotels table
CREATE TABLE hotels (
    hotel_id INT PRIMARY KEY,
    hotel_name VARCHAR(255) NOT NULL,
    hotel_formerly_name VARCHAR(255),
    translated_name VARCHAR(255),
    star_rating FLOAT,
    continent_id INT,
    country_id INT REFERENCES cities(country_id) ON DELETE SET NULL,
    city_id INT REFERENCES cities(city_id) ON DELETE SET NULL,
    area_id INT,
    longitude FLOAT,
    latitude FLOAT,
    hotel_url TEXT,
    popularity_score INT,
    remark TEXT,
    number_of_reviews INT,
    rating_average FLOAT,
    accommodation_type VARCHAR(50),
    nationality_restrictions TEXT,
    single_room_property BOOLEAN
);

-- Child and extra bed policy
CREATE TABLE child_policies (
    hotel_id INT PRIMARY KEY REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    infant_age INT,
    children_age_from INT,
    children_age_to INT,
    children_stay_free BOOLEAN,
    min_guest_age INT
);

-- Addresses table
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    hotel_id INT REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    address_type VARCHAR(50),
    address_line_1 TEXT,
    address_line_2 TEXT,
    postal_code VARCHAR(20),
    state VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100)
);

-- Hotel descriptions
CREATE TABLE hotel_descriptions (
    hotel_id INT PRIMARY KEY REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    overview TEXT,
    snippet TEXT
);

-- Facilities table
CREATE TABLE facilities (
    id SERIAL PRIMARY KEY,
    hotel_id INT REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    property_group_description VARCHAR(255),
    property_id INT,
    property_name VARCHAR(255),
    property_translated_name VARCHAR(255)
);

-- Pictures table
CREATE TABLE pictures (
    id SERIAL PRIMARY KEY,
    hotel_id INT REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    picture_id BIGINT,
    caption TEXT,
    caption_translated TEXT,
    url TEXT
);

-- Room types table
CREATE TABLE room_types (
    id SERIAL PRIMARY KEY,
    hotel_id INT REFERENCES hotels(hotel_id) ON DELETE CASCADE,
    hotel_room_type_id BIGINT,
    standard_caption TEXT,
    standard_caption_translated TEXT,
    max_occupancy_per_room INT,
    no_of_room INT,
    size_of_room FLOAT,
    room_size_incl_terrace BOOLEAN,
    views TEXT,
    max_extrabeds INT,
    max_infant_in_room INT,
    hotel_room_type_picture TEXT,
    bed_type TEXT,
    hotel_master_room_type_id BIGINT,
    hotel_room_type_alternate_name TEXT,
    shared_bathroom BOOLEAN,
    smoking_nonsmoking VARCHAR(50),
    gender VARCHAR(50)
);

-- Room type pictures table
CREATE TABLE room_type_pictures (
    id SERIAL PRIMARY KEY,
    room_type_id INT REFERENCES room_types(id) ON DELETE CASCADE,
    picture_url TEXT
);

-- Create indexes for better query performance
CREATE INDEX idx_hotels_city_id ON hotels(city_id);
CREATE INDEX idx_hotels_star_rating ON hotels(star_rating);
CREATE INDEX idx_hotels_popularity_score ON hotels(popularity_score);
CREATE INDEX idx_addresses_hotel_id ON addresses(hotel_id);
CREATE INDEX idx_facilities_hotel_id ON facilities(hotel_id);
CREATE INDEX idx_pictures_hotel_id ON pictures(hotel_id);
CREATE INDEX idx_room_types_hotel_id ON room_types(hotel_id);


where we put all of our hotel information, there is only static data for now which we have to update periodically by endpoint which will be the next task, for now
we need to implement a solution which help us to have an api for frontend to get all hotel data and load it on the web.

we have content static database but we need to get live data from partner api, we call it availability api where comes prices for rooms for specific searchs.
lets sey room for 4 person for specific dates. request looks like this 


https://sandbox-affiliateapi.agoda.com/api/v4/property/availability?apikey=API_KEY&mdate=20240901&mtypeid=1&siteID=1923846

thats what we request from backend.

and we get response like this 


    "searchId": 1659072373531790000,
    "properties": [
        {
            "propertyId": 1193699,
            "propertyName": "Jeju Central City",
            "translatedPropertyName": "Jeju Central City",
            "propertyUtcOffset": "+09:00",
            "rooms": [
                {
                    "roomId": 34007051,
                    "blockId": "OWMxZWUzNWMtM2ViOC1hNjhlLWJiN2ItYWQ3ZjIzMTFiMzM1OjMzMg==",
                    "roomName": "Family Twin Room - Non-Smoking",
                    "parentRoomName": "Family Twin Room - Non-Smoking",
                    "translatedRoomName": "Family Twin Room - Non-Smoking",
                    "blockIdBackup": "9c1ee35c-3eb8-a68e-bb7b-ad7f2311b335",
                    "parentRoomId": 34007051,
                    "ratePlanId": 513625,
                    "freeWifi": true,
                    "remainingRooms": 10,
                    "normalBedding": 4,
                    "extraBeds": 0,
                    "freeBreakfast": false,
                    "freeCancellation": true,
                    "totalPayment": {
                        "exclusive": 427.8,
                        "inclusive": 470.6,
                        "tax": 42.80,
                        "fees": 0.00,
                        "taxDueSupplier": 0,
                        "estimatedCommission": 0.00
                    },
                    "roomTypeNotGuaranteed": false,
                    "paymentModel": "Merchant",
                    "rate": {
                        "currency": "USD",
                        "exclusive": 85.56,
                        "inclusive": 94.12,
                        "tax": 8.56,
                        "fees": 0.00,
                        "method": "PRPN"

this is a small part I provide full response later


here is what frontend send us as a request

{
  "checkIn": "2024-09-22",
  "checkOut": "2024-09-23",
  "rooms": 1,
  "adults": 2,
  "children": 2,
  "cityId": 78471
}

of course city id is changing time by time.

ok so our goal is to return all data back to frontend included price and all hotel content start from description, rating, etc which comes from our database.

we want to make it on fastapi