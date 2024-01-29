import typer

from .client import app as client_app
from .server import app as server_app

app = typer.Typer()
app.add_typer(client_app, name="client")
app.add_typer(server_app, name="server")

if __name__ == "__main__":
    app()
