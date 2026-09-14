from typing import Dict,Any


from weather_mcp.domain.exceptions import ProviderError
from weather_mcp.domain.models import (
    CurrentWeather,
    DailyWeather,
    Location,
    WeatherForecast
)
from weather_mcp.domain.weather_codes import describe_weather_code
from weather_mcp.infrastructure.open_meteo.client import OpenMeteoClient
from weather_mcp.providers.weather import WeatherProvider
from weather_mcp.config import FORECAST_URL

class OpenMeteoWeather(WeatherProvider):

    def __init__(self,client:OpenMeteoClient)->None:
        self._client=client

    async def forecast(self,location:Location,*,days:int=7)->WeatherForecast:

        if not 1 <= days <= 15:
            raise ValueError(f"时间必须位于1~15之间")

        data=await self._client.get(
            url=FORECAST_URL,
            params={
                "latitude": location.latitude,
                "longitude": location.longitude,
                "current": ",".join(
                    [
                        "temperature_2m",
                        "apparent_temperature",
                        "relative_humidity_2m",
                        "precipitation",
                        "wind_speed_10m",
                        "wind_direction_10m",
                        "weather_code",
                    ]
                ),
                "daily": ",".join(
                    [
                        "weather_code",
                        "temperature_2m_max",
                        "temperature_2m_min",
                        "precipitation_sum",
                        "precipitation_probability_max",
                        "sunrise",
                        "sunset",
                    ]
                ),
                "forecast_days": days,
                "timezone": "auto",
            },
        )

        try:
            current=self._parse_daily(data=data)
            daily=self._parse_daily(data=data)
        except (KeyError,IndexError,TypeError) as ex:
                raise ProviderError(f"获取天气错误:{ex}")

        return WeatherForecast(location=location,current=current,daily=daily)


    @staticmethod
    def _parse_current(data:Dict[str,Any])->CurrentWeather:

        current = data["current"]
        units = data["current_units"]

        code = current["weather_code"]

        return CurrentWeather(
            time=current["time"],
            temperature=current["temperature_2m"],
            apparent_temperature=(
                current["apparent_temperature"]
            ),
            humidity=(
                current["relative_humidity_2m"]
            ),
            precipitation=current["precipitation"],
            wind_speed=current["wind_speed_10m"],
            wind_direction=(
                current["wind_direction_10m"]
            ),
            weather_code=code,
            weather_description=(
                describe_weather_code(code)
            ),
            temperature_unit=(
                units["temperature_2m"]
            ),
            wind_speed_unit=(
                units["wind_speed_10m"]
            ),
        )

    @staticmethod
    def _parse_daily(
        data: dict,
    ) -> list[DailyWeather]:

        daily = data["daily"]

        result: list[DailyWeather] = []

        for i, date in enumerate(
            daily["time"]
        ):

            code = daily["weather_code"][i]

            result.append(
                DailyWeather(
                    date=date,
                    weather_code=code,
                    weather_description=(
                        describe_weather_code(code)
                    ),
                    temperature_max=(
                        daily["temperature_2m_max"][i]
                    ),
                    temperature_min=(
                        daily["temperature_2m_min"][i]
                    ),
                    precipitation_sum=(
                        daily["precipitation_sum"][i]
                    ),
                    precipitation_probability_max=(
                        daily[
                            "precipitation_probability_max"
                        ][i]
                    ),
                    sunrise=daily["sunrise"][i],
                    sunset=daily["sunset"][i],
                )
            )

        return result