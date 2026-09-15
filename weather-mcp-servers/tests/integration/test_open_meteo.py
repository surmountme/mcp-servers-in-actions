from src.weather_mcp.clients.open_meteo.client import OpenMeteoClient
from src.weather_mcp.clients.open_meteo.geocoding import OpenMeteoGeocoding
from src.weather_mcp.clients.open_meteo.weather import OpenMeteoWeather


async def test_open_meteo():
    client = OpenMeteoClient()

    try:

        geocoding = OpenMeteoGeocoding(
            client
        )

        weather = OpenMeteoWeather(
            client
        )

        locations = await geocoding.search(
            "Beijing",
            count=1,
        )

        assert locations

        forecast = await weather.forecast(
            locations[0],
            days=3,
        )

        assert forecast.location.name

        assert len(forecast.daily) == 3

    finally:

        await client.close()
