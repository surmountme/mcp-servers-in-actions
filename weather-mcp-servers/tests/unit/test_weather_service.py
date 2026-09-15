from typing import List
from weather_mcp.services.weather_service import WeatherService
from weather_mcp.models.models import (
    CurrentWeather,
    DailyWeather,
    Location,
    WeatherForecast,
)
from weather_mcp.providers.geocoding import GeocodingProvider
from weather_mcp.providers.weather import WeatherProvider


class FakeGeocodingProvider(GeocodingProvider):

    async def search(self, name: str, *, count: int = 10, language: str = "en", format: str = "json", country_code: str = "CN") -> List[Location]:
        return [
            Location(
                name="Beijing",
                latitude=39.9042,
                longitude=116.4074,
                elevation=23,
                country="China",
                country_code="CN",
                admin1="Beijing",
                admin2="Beijing",
                timezone="Asia/Shanghai"
            )
        ]


class FakeWeatherProvider(WeatherProvider):

    async def forecast(self, location: Location, *, days: int = 7) -> WeatherForecast:
        return WeatherForecast(
            location=location,
            current=CurrentWeather(
                time="2026-09-15T22:00",
                temperature=25.0,
                precipitation=0.0,
                wind_speed=10.0,
                wind_direction=180.0,
                relative_humidity=50.0,
                apparent_temperature=26.0,
                weather_code=0,
                weather_description="Clear sky",
                temperature_unit="°C",
                wind_speed_unit="km/h",
                precipitation_unit="mm",
                relative_humidity_unit="%",
                apparent_temperature_unit="°C"
            ),
            daily=[
                DailyWeather(
                    date="2026-09-15",
                    weather_code=0,
                    weather_description="Clear sky",
                    sunrise_time="2026-09-15T05:38",
                    sunset_time="2026-09-15T18:00",
                    temperature_max=29.6,
                    temperature_min=22.5,
                    precipitation_sum=0.0,
                    precipitation_probability_max=0.0
                )
            ],
        )


async def test_get_forecast():
    service = WeatherService(
        geocoding_provider=FakeGeocodingProvider(),
        weather_provider=FakeWeatherProvider(),
    )
    city_name = "beijing"
    current_temperature = 25.0
    weather_description = "Clear sky"

    result = await service.get_forecast(city=city_name)

    assert result.location.name.lower() == city_name, f"断言城市名失败"
    assert result.current.temperature == current_temperature, f"期望结果为{current_temperature},实际结果为:{result.current.temperature}"
    assert result.current.weather_description == weather_description, f"期望结果为{weather_description},实际结果为：{result.current.weather_description}"
