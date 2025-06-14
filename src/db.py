import os
import logging
from typing import Any

from sqlalchemy import Column, Integer, String, Numeric, JSON, TIMESTAMP, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DB_URL", "postgresql+asyncpg://user:password@localhost/db")

Base = declarative_base()


class AccountBalance(Base):
    __tablename__ = "account_balances"

    id = Column(Integer, primary_key=True)
    broker = Column(String, nullable=False)
    balance = Column(Numeric, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    broker = Column(String, nullable=False)
    trade_id = Column(String, unique=True, nullable=False)
    data = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


def get_engine():
    return create_async_engine(DATABASE_URL, echo=False)


def get_session_factory(engine):
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def insert_account_balance(
    session: AsyncSession, broker: str, balance: Any
) -> None:
    record = AccountBalance(broker=broker, balance=balance)
    session.add(record)
    await session.commit()


async def insert_trades(session: AsyncSession, broker: str, trades: list[dict]) -> None:
    for trade in trades:
        record = Trade(broker=broker, trade_id=trade["id"], data=trade)
        session.add(record)
    await session.commit()
