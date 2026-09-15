from typing import Dict, List, Any
from mcp.server import MCPServer

from weather_mcp.bootstrap import create_application

app = create_application()

mcp = MCPServer(
    name="Weather MCP",
    description="用于获取当前和未来几天天气预报数据",
    instructions="用于查询当前和未来几天的天气预报数据"
)


@mcp.tool()
async def search_location(city: str, country_code: str = "CN") -> Dict[str, List[Dict[str, Any]]]:
    """
    通过城市名称来获取其位置信息
    :param city: 想要获取位置信息的城市名称，例如 beijing、shanghai、shenzhen 等
    :param country_code: 想要获取位置信息的城市所在国家，仅支持两个字母大写的缩写形式，并符合 ISO 3166-1 alpha-2 的标准，例如CN、US、JP等
    :return: 返回位置信息，示例：{"locations":[{"name":"shanghai","latitude":31.23,"longitude":123.31,"elevation":12,"country":"CN"}]}

    """

    return await app.weather_tools.search_location(city=city, country_code=country_code)


# @mcp.tool()
async def get_weather(city: str, days: int = 7, country_code: str = "CN") -> Dict[str, Any]:
    """
    通过城市名称获取当前天气和未来几天的天气预报
    :param city: 想要获取天气信息的城市名称，例如 beijing、shanghai、shenzhen 等
    :param days: 获取未来几天天气预报的天数设定，默认为未来7天，并且包含当天的，可以范围在1到16天之间，即[1,16]，其他暂不允许
    :param country_code: 想要获取天气信息的城市所在国家，仅支持两个字母大写的缩写形式，并符合 ISO 3166-1 alpha-2 的标准，例如CN、US、JP等
    :return: 返回天气信息，示例：{"location": {"locations": [{"name": "shanghai","latitude": 31.23,"longitude": 123.31,"elevation": 12,"country": "CN"}]},"current": {"date": "2026-09-15","weather_code": 1,"weather_description": "Clear Sky","sunrise_time": "2026-09-15T05:38","precipitation_probability_max": 80},"daily": {"time": "2026-09-15T19:45","temperature": 25.2,"precipitation": 0.0,"wind_speed": 10.0,"temperature_unit": "°C"}}
    """

    return await app.weather_tools.get_weather(city=city, days=days, country_code=country_code)


def main() -> None:
    mcp.run(transport="streamable-http", port=20149)


if __name__ == "__main__":
    # main()
    get_weather(city="shanghai")
