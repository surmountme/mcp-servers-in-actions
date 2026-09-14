from typing import List
from abc import ABC,abstractmethod

from weather_mcp.domain.models import Location

class GeocodingProvider(ABC):

    @abstractmethod
    async def search(self,name:str,*,count:int=5,language:str="en",format:str="json")->List[Location]:
        """根据名字搜索经纬度"""
        raise NotImplementedError