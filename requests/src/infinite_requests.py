"""
Script to make infinite requests to endpoint
"""

import asyncio
import click
from aiohttp import ClientSession, TCPConnector
from pypeln import asyncio_task as aio
from itertools import repeat


async def fetch(url, session):
    """
    Make an async request
    """
    async with session.get(url) as response:
        await response.read()
        print(response._body)


@click.command()
@click.option("--task-limit", default=100, help="Limit of concurrent tasks")
@click.option("--url", default="http://endpoint:80/", help="url to send requests")
def main(task_limit, url):
    """
    CLI main function
    """
    urls = repeat(url)
    aio.each(
        fetch,
        urls,
        workers=task_limit,
        on_start=lambda: ClientSession(connector=TCPConnector(limit=None)),
        on_done=lambda _status, session: session.close(),
        run=True,
    )


if __name__ == "__main__":
    main()
