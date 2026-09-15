from weather_mcp.clients.open_meteo.client import OpenMeteoClient
from weather_mcp.clients.open_meteo.geocoding import OpenMeteoGeocoding
from weather_mcp.clients.open_meteo.weather import OpenMeteoWeather


async def test_open_meteo():
    client = OpenMeteoClient()

    try:
        city_name = "beijing"
        days = 7
        geocoding = OpenMeteoGeocoding(client=client)
        weather = OpenMeteoWeather(client=client)
        locations = await geocoding.search(name=city_name, count=1)
        assert locations, f"locations断言失败"
        forecast = await weather.forecast(locations[0], days=days)
        assert forecast.location.name.lower() == city_name.lower(), f"实际返回的城市名为:{forecast.location.name.lower()}"
        assert len(forecast.daily) == days, f"实际返回的未来的天气数量失败，实际返回天数为{len(forecast.daily)}"

    finally:
        await client.close()
