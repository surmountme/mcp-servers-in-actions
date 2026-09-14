from typing import List
from weather_mcp.domain.exceptions import LocationNotFoundError
from weather_mcp.domain.models import (Location,WeatherForecast)
from weather_mcp.providers.geocoding import GeocodingProvider
from weather_mcp.providers.weather import WeatherProvider


class WeatherService():

    def __init__(self,geocoding_provider:GeocodingProvider,weather_provider:WeatherProvider)->None:
        self._geocoding=geocoding_provider
        self._weather =weather_provider

    async def search_location(self,city:str,*,count:int=5,language:str="en",format:str="json")->List[Location]:
        if not city:
            raise ValueError(f"城市不允许为空")

        return await self._geocoding.search(name=city,count=count,language=language,format=format)

    async def get_forecast(self,city:str,*,count:int=5,language:str="en",format:str="json",days:int=7)->WeatherForecast:

        locations=await self._geocoding.search(name=city,count=count,language=language,format=format)

        if not locations:
            raise LocationNotFoundError(f"查找{city}失败")

        return await self._weather.forecast(location=locations[0],days=days)