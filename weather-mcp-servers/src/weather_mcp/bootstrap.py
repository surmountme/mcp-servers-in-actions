from typing import Optional

from dataclasses import dataclass

from weather_mcp.services.weather_service import WeatherService
from weather_mcp.config import Settings
from weather_mcp.clients.open_meteo.client import OpenMeteoClient
from weather_mcp.clients.open_meteo.geocoding import OpenMeteoGeocoding
from weather_mcp.clients.open_meteo.weather import OpenMeteoWeather
from weather_mcp.tools.tools import WeatherTools


@dataclass
class Application:
    settings: Settings
    http_client: OpenMeteoClient
    weather_service: WeatherService
    weather_tools: WeatherTools

    async def close(self) -> None:
        await self.http_client.close()


def create_application(settings: Optional[Settings] = None, ) -> Application:
    settings = settings or Settings()
    http_client = OpenMeteoClient(timeout=settings.http_timeout)
    geocoding_provider = OpenMeteoGeocoding(client=http_client)
    weather_provider = OpenMeteoWeather(client=http_client)

    weather_service = WeatherService(
        geocoding_provider=geocoding_provider,
        weather_provider=weather_provider,
    )

    weather_tools = WeatherTools(service=weather_service)

    return Application(
        settings=settings,
        http_client=http_client,
        weather_service=weather_service,
        weather_tools=weather_tools,
    )
