import asyncio
from aiohttp import ClientSession, TCPConnector
from pypeln import asyncio_task as aio
from itertools import repeat

limit = 10
urls = repeat("http://localhost:3000/")


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


aio.each(
    fetch,
    urls,
    workers=limit,
    on_start=lambda: ClientSession(connector=TCPConnector(limit=None)),
    on_done=lambda _status, session: session.close(),
    run=True,
)