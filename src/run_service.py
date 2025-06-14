import asyncio
import logging

from .db import Base, get_engine, get_session_factory
from .scheduler import Scheduler

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    engine = get_engine()
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = get_session_factory(engine)
    async with session_factory() as session:
        scheduler = Scheduler(session)
        try:
            await scheduler.poll()
        finally:
            await scheduler.close()


if __name__ == "__main__":
    asyncio.run(main())
