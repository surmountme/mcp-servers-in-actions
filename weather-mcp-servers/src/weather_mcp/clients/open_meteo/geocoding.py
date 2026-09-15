from typing import List
from weather_mcp.models.models import Location
from weather_mcp.models.exceptions import ProviderError
from weather_mcp.clients.open_meteo.client import OpenMeteoClient
from weather_mcp.providers.geocoding import GeocodingProvider
from weather_mcp.config import OPEN_METEO_GEOCODING_URL


class OpenMeteoGeocoding(GeocodingProvider):

    def __init__(self, client: OpenMeteoClient) -> None:
        self._client = client

    async def search(self, name: str, *, count: int = 10, language: str = "en", format: str = "json", country_code: str = "CN") -> List[Location]:
        """
        获取城市的经纬度信息
        :param name: 城市名称
        :param count: 返回的结果数量限制
        :param language: 返回的目标语言，只支持 lower-case
        :param format: 返回的结果格式
        :param country_code: 默认的国家代码
        :return:
        """
        if not name.strip():
            return []

        params = {
            "name": name,
            "count": count,
            "language": language,
            "format": format,
            "countryCode": country_code,
        }

        response = await self._client.get(url=OPEN_METEO_GEOCODING_URL, params=params)

        results = response.get("results", [])

        locations: List[Location] = []

        for item in results:
            try:
                locations.append(
                    Location(
                        name=item.get("name", ""),
                        latitude=item.get("latitude", 0.0),
                        longitude=item.get("longitude", 0.0),
                        elevation=item.get("elevation", 0.0),
                        country=item.get("country", ""),
                        country_code=item.get("country_code", ""),
                        admin1=item.get("admin1", ""),
                        admin2=item.get("admin2", ""),
                        timezone=item.get("timezone", "")

                    )
                )
            except KeyError as ex:
                raise ProviderError(f"获取 {name} 的位置信息出错 {ex}")

        return locations
