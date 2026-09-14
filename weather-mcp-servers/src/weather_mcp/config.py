
GEOCODING_URL:str= "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL :str= "https://api.open-meteo.com/v1/forecast"


from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:

    http_timeout: float = 10.0

    default_forecast_days: int = 3

    max_forecast_days: int = 16