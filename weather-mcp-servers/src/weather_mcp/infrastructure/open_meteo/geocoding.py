from typing import List
from weather_mcp.domain.models import Location
from weather_mcp.domain.exceptions import ProviderError
from weather_mcp.infrastructure.open_meteo.client import OpenMeteoClient
from weather_mcp.providers.geocoding import GeocodingProvider
from weather_mcp.config import GEOCODING_URL

class OpenMeteoGeocoding(GeocodingProvider):

    def __init__(self,client:OpenMeteoClient)->None:
        self._client=client

    async def search(self,name:str,*,count:int=5,language:str="en",format:str="json")->List[Location]:

        if not name.strip():
            return []

        data=await self._client.get(
                url=GEOCODING_URL,
                params={
                    "name":name,
                    "count":count,
                    "language":language,
                    "format":format
                }
            )

        results=data.get("results",[])

        locations:List[Location]=[]

        for item in results:
            try:
                locations.append(
                    Location(
                        name=item.get("name",""),
                        latitude=item.get("latitude",0.0),
                        longitude=item.get("longitude",0.0),
                        country=item.get("country",""),
                        state=item.get("admin1",""),
                        timezone=item.get("timezone","")
                    )
                )
            except KeyError as ex:
                raise ProviderError(f"获取{name}的经纬度信息出错{ex}")

        return locations