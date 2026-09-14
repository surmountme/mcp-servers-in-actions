from typing import List
from src.weather_mcp.application.weather_service import WeatherService
from src.weather_mcp.domain.models import (
    CurrentWeather,
    DailyWeather,
    Location,
    WeatherForecast,
)
from src.weather_mcp.providers.geocoding import GeocodingProvider
from src.weather_mcp.providers.weather import WeatherProvider


class FakeGeocodingProvider(GeocodingProvider):

    async def search(self,name: str,*,count: int = 5,) -> List[Location]:

        return [
            Location(
                name="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                timezone="Asia/Shanghai",
                country="China",
            )
        ]


class FakeWeatherProvider(WeatherProvider):

    async def forecast(self,location: Location,*,days: int = 3,) -> WeatherForecast:

        return WeatherForecast(
            location=location,
            current=CurrentWeather(
                time="2026-09-11T12:00",
                temperature=25.0,
                apparent_temperature=26.0,
                humidity=50.0,
                precipitation=0.0,
                wind_speed=10.0,
                wind_direction=180.0,
                weather_code=0,
                weather_description="Clear sky",
                temperature_unit="°C",
                wind_speed_unit="km/h",
            ),
            daily=[
                DailyWeather(
                    date="2026-09-11",
                    weather_code=0,
                    weather_description="Clear sky",
                    temperature_max=30.0,
                    temperature_min=20.0,
                    precipitation_sum=0.0,
                    precipitation_probability_max=0.0,
                    sunrise="05:30",
                    sunset="18:30",
                )
            ],
        )


async def test_get_forecast():

    service = WeatherService(
        geocoding_provider=(
            FakeGeocodingProvider()
        ),
        weather_provider=(
            FakeWeatherProvider()
        ),
    )

    result = await service.get_forecast(
        "Beijing"
    )

    assert result.location.name == "Beijing"

    assert result.current.temperature == 25.0

    assert (
        result.current.weather_description
        == "Clear sky"
    )