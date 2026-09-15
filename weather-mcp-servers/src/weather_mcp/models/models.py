from typing import Optional, List
from pydantic import BaseModel, Field


class Location(BaseModel):
    # 城市名称
    name: str
    # 纬度
    latitude: float
    # 经度
    longitude: float
    # 海拔
    elevation: int = 0
    # 国家
    country: str
    # 国家代码
    country_code: str
    # 一级和二级行政区域
    admin1: Optional[str] = None
    admin2: Optional[str] = None
    # 时区
    timezone: str


class CurrentWeather(BaseModel):
    # 当前时间
    time: str
    # 当前温度
    temperature: float
    # 降雨量
    precipitation: float
    # 风速
    wind_speed: float
    # 风向
    wind_direction: int
    # 相对湿度
    relative_humidity: float
    # 地表温度
    apparent_temperature: float
    # 天气代码
    weather_code: int
    # 天气详情
    weather_description: str

    # 温度单位
    temperature_unit: str
    # 风速单位
    wind_speed_unit: str
    # 降雨量单位
    precipitation_unit: str
    # 相对湿度单位
    relative_humidity_unit: str
    # 地表温度单位
    apparent_temperature_unit: str


class DailyWeather(BaseModel):
    # 日期
    date: str
    # 天气代码和详情
    weather_code: int
    weather_description: str
    # 日升和日落时间
    sunrise_time: str
    sunset_time: str
    # 最高和最低温度
    temperature_max: float
    temperature_min: float
    # 降雨量总和概率
    precipitation_sum: float
    precipitation_probability_max: Optional[float] = None


class WeatherForecast(BaseModel):
    location: Location
    current: CurrentWeather
    daily: List[DailyWeather] = Field(default_factory=list)
