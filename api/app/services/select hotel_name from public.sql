select hotel_name from public.hotels where hotel_id = 17072


SELECT address_line_1 FROM public.addresses WHERE hotel_id = 17072


SELECT json_object_agg(
    caption, urls
) AS grouped_pictures
FROM (
    SELECT caption, json_agg(url) AS urls
    FROM public.pictures
    WHERE hotel_id = 17072
    GROUP BY caption
) AS subquery;


SELECT longitude, latitude 
FROM public.hotels 
WHERE hotel_id = 17072;


SELECT json_agg(
         json_build_object(
             'property_group_description', property_group_description,
             'facilities', facilities
         )
       ) AS grouped_facilities
FROM (
    SELECT property_group_description, array_agg(property_name) AS facilities
    FROM public.facilities
    WHERE hotel_id = 17072
    GROUP BY property_group_description
) subquery;




