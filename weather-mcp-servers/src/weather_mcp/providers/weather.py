from abc import ABC,abstractmethod

from weather_mcp.domain.models import (Location,WeatherForecast)

class WeatherProvider(ABC):

    @abstractmethod
    async def forecast(self,location:Location,*,days:int=7)-> WeatherForecast:
        """获取天气预报"""
        raise NotImplementedError