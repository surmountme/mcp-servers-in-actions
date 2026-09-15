from dataclasses import dataclass

OPEN_METEO_GEOCODING_URL: str = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_FORECAST_URL: str = "https://api.open-meteo.com/v1/forecast"


@dataclass(frozen=True)
class Settings:
    http_timeout: float = 30.0
    default_forecast_days: int = 7
    max_forecast_days: int = 16
