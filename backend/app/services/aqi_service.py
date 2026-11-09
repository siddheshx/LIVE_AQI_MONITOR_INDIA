import httpx

OPEN_METEO_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


async def fetch_city_aqi(latitude: float, longitude: float):
    """
    Fetch modelled air-quality data for one geographic location.
    """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "pm2_5,pm10,us_aqi,european_aqi",
        "timezone": "Asia/Kolkata",
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            OPEN_METEO_URL,
            params=params,
        )

        response.raise_for_status()

        return response.json()


async def fetch_multiple_cities(cities: list):
    """
    Fetch air-quality data for multiple cities in one request.
    """

    if not cities:
        return []

    latitudes = ",".join(str(city.latitude) for city in cities)
    longitudes = ",".join(str(city.longitude) for city in cities)

    params = {
        "latitude": latitudes,
        "longitude": longitudes,
        "current": "pm2_5,pm10,us_aqi,european_aqi",
        "timezone": "Asia/Kolkata",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(
            OPEN_METEO_URL,
            params=params,
        )

        response.raise_for_status()

        data = response.json()

        # A single coordinate may return a JSON object.
        # Multiple coordinates normally return a list.
        if isinstance(data, dict):
            data = [data]

        return data