
class WeatherError(Exception):
    """Weather基础错误基类"""

class LocationNotFoundError(WeatherError):
    """当位置无法搜索到的错误基类"""

class ProviderError(WeatherError):
    """外部Provider失败的基类"""