
from typing import Optional,List
from pydantic import BaseModel, Field

class Location(BaseModel):
    name:str
    latitude:float
    longitude:float
    country:Optional[str]=None
    state:Optional[str]=None
    timezone:str

class CurrentWeather(BaseModel):
    time:str
    temperature:float
    # 表面温度
    apparent_temperature:float
    # 温度
    humidity:float
    # 降水
    precipitation:float
    # 风速
    wind_speed:float
    # 风向
    wind_direction:float

    weather_code:int
    weather_description:str

    temperature_unit:str
    wind_speed_unit:str

class DailyWeather(BaseModel):
    date:str
    weather_code:int
    weather_description:str

    temperature_max:float
    temperature_min:float

    precipitation_sum:float
    precipitation_probability_max:Optional[float]=None

    sunrise:str
    sunset:str

class WeatherForecast(BaseModel):
    location: Location
    current:CurrentWeather
    daily:List[DailyWeather]=Field(default_factory=list)