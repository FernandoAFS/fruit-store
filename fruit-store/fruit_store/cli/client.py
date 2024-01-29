import asyncio
import pathlib
import datetime as dt

import typer

from fruit_store.client import client as grpc_client

app = typer.Typer()


@app.command()
def purchase_event(date: "dt.datetime", item: str, quantity: int, price: float):
    client_ = grpc_client.FruitStoreClient()
    asyncio.run(client_.put_sale(date, item, quantity, price))
    return

# ADD OPTION TO SEND IN BULK OR NOT.
@app.command()
def purchase_event_json(files: list[pathlib.Path]):
    """
    Convenience method that inputs multiple
    """
    ...

@app.command()
def request_report(date_0: "dt.datetime", date_f: "dt.datetime"):
    client_ = grpc_client.FruitStoreClient()
    report = asyncio.run(client_.request_report(date_0, date_f))
    # TODO: PRETTY PRINT THE REPORT
    print(report)
    return

@app.command()
def healthcheck():
    client_ = grpc_client.FruitStoreClient()
    asyncio.run(client_.healthcheck())
    print("healthcheck ok")

if __name__ == "__main__":
    app()

