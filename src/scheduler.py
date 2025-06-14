import asyncio
import logging
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

from .db import insert_account_balance, insert_trades
from .clients.thinkorswim_api import ThinkOrSwimClient
from .clients.schwab_api import CharlesSchwabClient
from .clients.robinhood_api import RobinhoodClient
from .clients.webull_api import WebullClient

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.clients: Dict[str, object] = {
            "thinkorswim": ThinkOrSwimClient(),
            "schwab": CharlesSchwabClient(),
            "robinhood": RobinhoodClient(),
            "webull": WebullClient(),
        }
        self.last_trade_ids: Dict[str, str | None] = {
            name: None for name in self.clients.keys()
        }

    async def poll(self) -> None:
        while True:
            for name, client in self.clients.items():
                try:
                    balance = await client.fetch_balance()
                    if balance is not None:
                        await insert_account_balance(self.session, name, balance)
                except Exception as error:
                    logger.exception("Balance ingestion failed for %s: %s", name, error)

                try:
                    trades = await client.fetch_trades(self.last_trade_ids[name])
                    if trades:
                        await insert_trades(self.session, name, trades)
                        self.last_trade_ids[name] = trades[-1]["id"]
                except Exception as error:
                    logger.exception("Trade ingestion failed for %s: %s", name, error)

            await asyncio.sleep(5)

    async def close(self) -> None:
        for client in self.clients.values():
            await client.close()
