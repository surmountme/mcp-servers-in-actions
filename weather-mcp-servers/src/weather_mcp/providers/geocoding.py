from typing import List
from abc import ABC, abstractmethod

from weather_mcp.models.models import Location


class GeocodingProvider(ABC):

    @abstractmethod
    async def search(self, name: str, *, count: int = 10, language: str = "en", format: str = "json", country_code: str = "CN") -> List[Location]:
        """获取城市的经纬度信息"""
        raise NotImplementedError
