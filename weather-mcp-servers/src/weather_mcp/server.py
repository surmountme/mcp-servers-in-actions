from mcp.server import MCPServer

from weather_mcp.bootstrap import create_application


app = create_application()

mcp = MCPServer(
    "Weather MCP",
    instructions=(
        "Provides current weather and weather "
        "forecast information."
    ),
)


@mcp.tool()
async def search_location(
    city: str,
) -> dict:
    """
    Search for locations matching a city name.

    Args:
        city: City or location name.
    """

    return await app.weather_tools.search_location(
        city
    )


@mcp.tool()
async def get_weather(
    city: str,
    days: int = 3,
) -> dict:
    """
    Get current weather and daily forecast.

    Args:
        city: City or location name.
        days: Number of forecast days, from 1 to 16.
    """

    return await app.weather_tools.get_weather(
        city,
        days,
    )


def main() -> None:
    mcp.run(
        transport="stdio"
    )


if __name__ == "__main__":
    main()