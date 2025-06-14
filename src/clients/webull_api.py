import os
import logging
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class WebullClient:
    def __init__(self) -> None:
        self.token = os.getenv("WEBULL_TOKEN", "")
        self.base_url = "https://api.webull.com"
        self.session = aiohttp.ClientSession()

    async def fetch_balance(self) -> Any:
        url = f"{self.base_url}/balance"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            async with self.session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as error:
            logger.exception("Error fetching Webull balance: %s", error)
            return None

    async def fetch_trades(self, since_id: str | None = None) -> list[dict]:
        url = f"{self.base_url}/trades"
        params = {"since_id": since_id} if since_id else None
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            async with self.session.get(
                url, headers=headers, params=params
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as error:
            logger.exception("Error fetching Webull trades: %s", error)
            return []

    async def close(self) -> None:
        await self.session.close()
