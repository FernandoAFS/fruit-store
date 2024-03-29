import logging

import typer

from . import server as cli_server

app = typer.Typer()


@app.callback()
def main():
    logging.basicConfig(level=logging.INFO)


def add_client_app():
    from . import client

    app.add_typer(client.app, name="client")


add_client_app()


@app.command()
def version():
    "Print out the version"
    from fruit_store import __version__

    print(f"{__version__}")


@app.command()
def server(host: str = "[::]:50051"):
    "Spawns server daemon"
    cli_server.server(host)


if __name__ == "__main__":
    app()
