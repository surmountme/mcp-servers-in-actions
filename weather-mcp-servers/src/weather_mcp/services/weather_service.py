from typing import List
from weather_mcp.models.exceptions import LocationNotFoundError
from weather_mcp.models.models import (Location, WeatherForecast)
from weather_mcp.providers.geocoding import GeocodingProvider
from weather_mcp.providers.weather import WeatherProvider


class WeatherService():

    def __init__(self, geocoding_provider: GeocodingProvider, weather_provider: WeatherProvider) -> None:
        self._geocoding = geocoding_provider
        self._weather = weather_provider

    async def search_location(self, city: str, *, count: int = 10, language: str = "en", format: str = "json", country_code: str = "CN") -> List[Location]:
        if not city:
            raise ValueError(f"城市不允许为空")

        return await self._geocoding.search(name=city, count=count, language=language, format=format, country_code=country_code)

    async def get_forecast(self, city: str, *, count: int = 10, language: str = "en", format: str = "json", country_code: str = "CN", days: int = 7) -> WeatherForecast:

        locations = await self.search_location(name=city, count=count, language=language, format=format, country_code=country_code)
        print(f"locations:{locations}")
        if not locations:
            raise LocationNotFoundError(f"查找 {city} 位置失败")

        # for location in locations:
        # if location.country_code == country_code and city.lower() == location.name.lower() and location.admin2.lower().__contains__(city.lower()):
        return await self._weather.forecast(location=locations[0], days=days)
