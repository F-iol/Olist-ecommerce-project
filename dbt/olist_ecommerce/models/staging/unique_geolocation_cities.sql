{{ config(materialized='table') }}

SELECT 
  LOWER(REGEXP_REPLACE(REGEXP_REPLACE(geolocation_city, r"[£§¢ã]", "a"), r'\s+', '')) AS cleaned_name,
  COUNT(*) as occurrences
FROM {{ source('raw_data', 'olist_geolocation_dataset') }}
GROUP BY 1
ORDER BY occurrences DESC