Hotel Detailed Information
1. Hotel Name
select hotel_name from public.hotels where hotel_id = 147265
2. Hotel Address
PostgreSQL - 
SELECT address_line_1 
FROM public.addresses 
WHERE hotel_id = 147265;
3. Hotel All Images
hotel images are groupd by captions


get hotel all images group by captioned in json format with query:

````
SELECT json_object_agg(
    caption, urls
) AS grouped_pictures
FROM (
    SELECT caption, json_agg(url) AS urls
    FROM public.pictures
    WHERE hotel_id = 147265
    GROUP BY caption
) AS subquery;
````


output:

{
  "Bed"; [
    "https://pix8.agoda.net/hotelImages/147265/-1/5709a9756e24261be17a0e38b0f6c91c.jpg?ca=13&ce=1&s=312x",
    "https://pix8.agoda.net/hotelImages/147265/-1/0738b266804dedaae43d26bf3e1b54aa.jpg?ca=13&ce=1&s=312x",
    "https://pix8.agoda.net/hotelImages/147265/-1/5709a9756e24261be17a0e38b0f6c91c.jpg?ca=13&ce=1&s=312x",
    "https://pix8.agoda.net/hotelImages/147265/-1/0738b266804dedaae43d26bf3e1b54aa.jpg?ca=13&ce=1&s=312x",
    "https://pix8.agoda.net/hotelImages/147265/-1/5709a9756e24261be17a0e38b0f6c91c.jpg?ca=13&ce=1&s=312x",
    "https://pix8.agoda.net/hotelImages/147265/-1/0738b266804dedaae43d26bf3e1b54aa.jpg?ca=13&ce=1&s=312x"
  ],
  "Recreational facilities"; [
    "https://pix8.agoda.net/hotelImages/147/147265/147265_15083122570035463781.jpg?ca=5&ce=1&s=312x"
  ]
}


get unique names of captios with query


```
SELECT json_agg(DISTINCT caption) 
FROM public.pictures;
```

output
````
[
  "",
  "Amenity (Guest room)",
  "Attractions",
  "Balcony/terrace",
  "Ballroom",
]
```

4. All Amenites
We have an amenity categories, in api its called facilities not amenities so each facility has property_group_descriptions which are groups and used to group facilities. here are a list of groups

{
  "property_group_descriptions": [
    "Access",
    "Accessibility",
    "Services and conveniences",
    "Sports equipment rental",
    "Swimming & soaking",
    "Things to do, ways to relax"
  ]
}

To get all facilities groupd by property_group_descriptions in json format you can execute sql query

```
SELECT json_agg(
         json_build_object(
             'property_group_description', property_group_description,
             'facilities', facilities
         )
       ) AS grouped_facilities
FROM (
    SELECT property_group_description, array_agg(property_name) AS facilities
    FROM public.facilities
    WHERE hotel_id = 2937
    GROUP BY property_group_description
) subquery;
```

5. Hotel's available rooms detailed information from db (pictures, etc)
SELECT * 
FROM public.room_types 
WHERE hotel_id = 2937 
AND hotel_room_type_id = 3028166;


6. Map longitude and latitude information
SELECT longitude, latitude 
FROM public.hotels 
WHERE hotel_id = 2937;