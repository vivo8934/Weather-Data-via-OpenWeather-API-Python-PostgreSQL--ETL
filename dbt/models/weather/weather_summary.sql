SELECT DISTINCT ON (city)
  city,
  region,
  temperature_c,
  condition,
  humidity,
  wind_kph,
  local_time
FROM {{ ref('weather_data') }}
ORDER BY city, local_time DESC