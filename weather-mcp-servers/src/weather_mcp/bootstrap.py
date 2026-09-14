from dataclasses import dataclass

from weather_mcp.application.weather_service import WeatherService
from weather_mcp.config import Settings
from weather_mcp.infrastructure.open_meteo.client import OpenMeteoClient
from weather_mcp.infrastructure.open_meteo.geocoding import OpenMeteoGeocoding
from weather_mcp.infrastructure.open_meteo.weather import  OpenMeteoWeather
from weather_mcp.mcp.tools import WeatherTools

@dataclass
class Application:

    settings: Settings

    http_client: OpenMeteoClient

    weather_service: WeatherService

    weather_tools: WeatherTools

    async def close(self) -> None:
        await self.http_client.close()


def create_application(
    settings: Settings | None = None,
) -> Application:

    settings = settings or Settings()

    http_client = OpenMeteoClient(
        timeout=settings.http_timeout,
    )

    geocoding_provider = OpenMeteoGeocoding(
        http_client
    )

    weather_provider = OpenMeteoWeather(
        http_client
    )

    weather_service = WeatherService(
        geocoding_provider=geocoding_provider,
        weather_provider=weather_provider,
    )

    weather_tools = WeatherTools(
        weather_service
    )

    return Application(
        settings=settings,
        http_client=http_client,
        weather_service=weather_service,
        weather_tools=weather_tools,
    )