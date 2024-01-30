import asyncio

import typer


def server(host: str = "[::]:50051"):
    "Spawns server daemon"
    from fruit_store.server import async_serve

    asyncio.run(async_serve.serve(host))


if __name__ == "__main__":
    typer.run(server)
