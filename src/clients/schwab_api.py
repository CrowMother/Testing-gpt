import os
import logging
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)


class CharlesSchwabClient:
    def __init__(self) -> None:
        self.token = os.getenv("SCHWAB_TOKEN", "")
        self.client_id = os.getenv("SCHWAB_CLIENT_ID", "")
        self.client_secret = os.getenv("SCHWAB_CLIENT_SECRET", "")
        self.base_url = "https://api.schwab.com"
        self.authorization_url = "https://api.schwab.com/oauth2/authorize"
        self.token_url = "https://api.schwab.com/oauth2/token"
        self.session = aiohttp.ClientSession()

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        """Return the OAuth authorization URL for user login."""
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "state": state,
            "scope": "accounts trading",
        }
        url = aiohttp.client.URL("/", encoded=True).with_query(params)
        query_string = url.query_string
        return f"{self.authorization_url}?{query_string}"

    async def exchange_code(self, code: str, redirect_uri: str) -> bool:
        """Exchange an authorization code for an access token."""
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        try:
            async with self.session.post(
                self.token_url,
                data=data,
            ) as response:
                response.raise_for_status()
                payload = await response.json()
                self.token = payload.get("access_token", "")
                return bool(self.token)
        except Exception as error:  # broad exception for example
            logger.exception("Token exchange failed: %s", error)
            return False

    async def fetch_balance(self) -> Any:
        url = f"{self.base_url}/balance"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            async with self.session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as error:
            logger.exception(
                "Error fetching Charles Schwab balance: %s",
                error,
            )
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
            logger.exception("Error fetching Charles Schwab trades: %s", error)
            return []

    async def close(self) -> None:
        await self.session.close()
