import asyncio
import logging

import typer

from fruit_store.server import async_serve

@typer.command()
def server():
    logging.basicConfig(level=logging.INFO)
    asyncio.run(async_serve.serve())


if __name__ == "__main__":
    server()
