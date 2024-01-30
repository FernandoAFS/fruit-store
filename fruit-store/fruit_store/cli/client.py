import asyncio
import datetime as dt
import json
import pathlib

import typer

from fruit_store.client import client as grpc_client

app = typer.Typer()

app_state = {}


@app.callback()
def main(host: str = "localhost:50051"):
    app_state["host"] = host


@app.command()
def purchase_event(date: "dt.datetime", item: str, quantity: int, price: float):
    client_ = grpc_client.FruitStoreClient(app_state["host"])
    asyncio.run(client_.put_sale(date, quantity, item, price))
    return


def path_to_dict(p: pathlib.Path):
    with p.open("rb") as f:
        j = json.load(f)
    d = dt.datetime.fromisoformat(j["date"])
    return {
        **j,
        "date": d,
    }




# ADD OPTION TO SEND IN BULK OR NOT.
@app.command()
def purchase_event_json(files: list[pathlib.Path]):
    """
    Convenience method that inputs multiple
    """
    client_ = grpc_client.FruitStoreClient(app_state["host"])
    jsons = map(path_to_dict, files)

    for j in jsons:
        asyncio.run(client_.put_sale(**j))


@app.command()
def request_report(date_0: "dt.datetime", date_f: "dt.datetime"):
    client_ = grpc_client.FruitStoreClient(app_state["host"])
    report = asyncio.run(client_.request_report(date_0, date_f))
    # TODO: PRETTY PRINT THE REPORT
    print(report)
    return


@app.command()
def healthcheck():
    try:
        client_ = grpc_client.FruitStoreClient(app_state["host"])
        hc = asyncio.run(client_.healthcheck())

        if not hc:
            print("HC not ok")
            raise typer.Exit(code=1)
    except Exception as e:
        raise e

    print("healthcheck ok")


if __name__ == "__main__":
    app()
