from typing import Dict, List, Any
from weather_mcp.services.weather_service import WeatherService


class WeatherTools:

    def __init__(self, service: WeatherService) -> None:
        self._serive = service

    async def search_location(self, city: str, *, count: int = 10, language: str = "en", format: str = "json", country_code: str = "CN") -> Dict[List[Dict[str, Any]]]:
        locations = await self._serive.search_location(city=city, count=count, language=language, format=format, country_code=country_code)

        return {"locations": [location.model_dump() for location in locations]}

    async def get_weather(self, city: str, days: int = 7, count: int = 10, language: str = "en", format: str = "json", country_code: str = "CN") -> Dict[str, Any]:
        forecast = await self._serive.get_forecast(city=city, count=count, language=language, format=format, country_code=country_code, days=days)

        return forecast.model_dump()
