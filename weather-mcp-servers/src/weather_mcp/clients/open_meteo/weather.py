from typing import Dict, List, Union, Any
from unittest import result

from weather_mcp.models.exceptions import ProviderError
from weather_mcp.models.models import (
    CurrentWeather,
    DailyWeather,
    Location,
    WeatherForecast
)
from weather_mcp.models.weather_codes import describe_weather_code
from weather_mcp.clients.open_meteo.client import OpenMeteoClient
from weather_mcp.providers.weather import WeatherProvider
from weather_mcp.config import OPEN_METEO_FORECAST_URL


class OpenMeteoWeather(WeatherProvider):

    def __init__(self, client: OpenMeteoClient) -> None:
        self._client = client

    async def forecast(self, location: Location, *, days: int = 7) -> WeatherForecast:
        """查询天气预报"""
        if not 1 <= days <= 16:
            raise ValueError(f"查询的时间范围必须位于1~16之间")
        # 查询天气预报的参数，详细参数可查阅官网 https://open-meteo.com/en/docs
        params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "current": ",".join(
                [
                    "temperature_2m",
                    "precipitation",
                    "weather_code",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "relative_humidity_2m",
                    "rain",
                    "apparent_temperature"
                ]
            ),
            "daily": ",".join(
                [
                    "weather_code",
                    "sunrise",
                    "sunset",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                    "precipitation_probability_max",

                ]
            ),
            "forecast_days": days,
            "timezone": "auto",
        }

        response = await self._client.get(url=OPEN_METEO_FORECAST_URL, params=params)

        try:
            current = self._parse_current(data=response)
            daily = self._parse_daily(data=response)
        except (KeyError, IndexError, TypeError) as ex:
            raise ProviderError(f"获取天气错误:{ex}")

        return WeatherForecast(location=location, current=current, daily=daily)

    @staticmethod
    def _parse_current(data: Dict[str, Any]) -> CurrentWeather:
        """获取当前时间的天气预报"""

        current: Dict[str, Any] = data.get("current", {})
        units: Dict[str, Any] = data.get("current_units", {})
        weather_code: int = current.get("weather_code", -999)
        current_weather_result = CurrentWeather(
            time=current.get("time", "1900-01-01T00:00"),
            temperature=current.get("temperature_2m", -999.00),
            precipitation=current.get("precipitation", 0.00),
            wind_speed=current.get("wind_speed_10m", 0.00),
            wind_direction=current.get("wind_direction_10m", 0),
            relative_humidity=current.get("relative_humidity_2m", 0.00),
            apparent_temperature=current.get("apparent_temperature", -999.00),
            weather_code=weather_code,
            weather_description=describe_weather_code(weather_code),

            temperature_unit=units.get("temperature_2m", "°C"),
            wind_speed_unit=units.get("wind_speed_10m", "km/h"),
            precipitation_unit=units.get("precipitation", "mm"),
            relative_humidity_unit=units.get("relative_humidity_2m", "%"),
            apparent_temperature_unit=units.get("apparent_temperature", "°C")
        )
        return current_weather_result

    @staticmethod
    def _parse_daily(data: Dict[str, Any]) -> List[DailyWeather]:
        """获取每天的天气预报"""

        daily: Dict[str, Dict[str, List[Union[str, int, float]]]] = data.get("daily", {})

        daily_weather_result: List[DailyWeather] = []

        for idx, date in enumerate(daily.get("time", [])):
            code = daily.get("weather_code", [])[idx]
            daily_weather_result.append(
                DailyWeather(
                    date=date,
                    weather_code=code,
                    weather_description=describe_weather_code(code),
                    sunrise_time=daily.get("sunrise", [])[idx],
                    sunset_time=daily.get("sunset", [])[idx],
                    temperature_max=daily.get("temperature_2m_max", [])[idx],
                    temperature_min=daily.get("temperature_2m_min", [])[idx],
                    precipitation_sum=daily.get("precipitation_sum", [])[idx],
                    precipitation_probability_max=daily.get("precipitation_probability_max", [])[idx]
                )
            )

        return daily_weather_result
