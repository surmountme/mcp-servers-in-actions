from typing import Dict,Any

import httpx

from weather_mcp.domain.exceptions import ProviderError


class OpenMeteoClient():

    def __init__(self, *, timeout: float = 30.0) -> None:
        self._client = httpx.AsyncClient(
            headers={
                "User-Agent": "weather-mcp-servers/0.1.0"
            },
            timeout=timeout
        )

    async def get(self,url:str,*,params:Dict[str,Any])->Dict[str,Any]:

        try:
            response=await self._client.get(url=url,params=params)
        except httpx.HTTPError as ex:
            raise ProviderError(f"请求OpenMeteo失败：{ex}")

        try:
            return response.json()
        except ValueError as ex:
            raise ProviderError(f"OpenMeteo返回的数据不是JSON格式")

    async def close(self)->None:
        await self._client.aclose()