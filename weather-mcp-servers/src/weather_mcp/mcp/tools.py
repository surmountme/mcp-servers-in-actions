from typing import Dict,List,Any
from weather_mcp.application.weather_service import WeatherService


class WeatherTools:

    def __init__(self,service:WeatherService)->None:
        self._serive=service

    async def search_location(self,city:str,*,count:int=5,language:str="en",format:str="json")->Dict[List[Dict[str,Any]]]:

        locations=await self._serive.search_location(city=city,count=5,language=language,format=format)

        return {
            "locations":[ location.model_dump for location in locations ]
        }

    async def get_weather(self,city:str,days:int=7,count:int=5,language:str="en",format:str="json")->Dict[str,Any]:

        forecast=(await self._serive.get_forecast(
            city=city,count=count,language=language,format=format,days=days
        ))

        return forecast.model_dump()