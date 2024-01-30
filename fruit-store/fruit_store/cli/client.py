import asyncio
import datetime as dt
import itertools as it
import json
import math
import pathlib
import typing as t

import typer

app = typer.Typer()

app_state = {}


@app.callback()
def main(host: str = "localhost:50051"):
    app_state["host"] = host


@app.command()
def purchase_event(date: "dt.datetime", item: str, quantity: int, price: float):
    """
    Send a purchase event directly from the cli
    """
    from fruit_store.client import client as grpc_client
    from fruit_store.grpc import factory

    client_ = grpc_client.FruitStoreClient(app_state["host"])
    event = factory.PurchaseEventModel(
        date=date, quantity=quantity, item=item, price=math.ceil(price * 100)
    )
    asyncio.run(client_.put_sale(event))
    return


def path_to_event(p: pathlib.Path):
    from fruit_store.grpc import factory

    with p.open("rb") as f:
        j = json.load(f)

    # CHECK IF ITS OBJECT OR LIST.

    def d_to_event(j: "t.Mapping[str, t.Any]") -> "factory.PurchaseEventModel":
        d = dt.datetime.fromisoformat(j["date"])  # type: ignore
        return factory.PurchaseEventModel.from_dict(
            {
                **j,
                "date": d,
            }
        )

    # ITS' SAFE TO ASSUME BASIC COLLECTIONS AS LONG AS WE ARE USING STANDARD
    # JSON PARSER
    match j:
        case list():
            yield from map(d_to_event, j)
            return
        case dict():
            yield d_to_event(j)
            return

    raise TypeError(f"Json type object {type(j)} not supported: {str(j)[:200]}")


# ADD OPTION TO SEND IN BULK OR NOT.
@app.command()
def purchase_event_json(files: list[pathlib.Path]):
    """
    Convenience method that inputs multiple json files and sends them as events
    """
    from fruit_store.client import client as grpc_client

    client_ = grpc_client.FruitStoreClient(app_state["host"])
    events = it.chain.from_iterable(map(path_to_event, files))

    # TODO: MAYBE USE BETTER WAY. BATCH REQUESTS OR EVEN DO GRPC STREAM
    for ev in events:
        asyncio.run(client_.put_sale(ev))


@app.command()
def request_report(
    date_0: "t.Annotated[t.Optional[dt.datetime], typer.Argument()]" = None,
    date_f: "t.Annotated[t.Optional[dt.datetime], typer.Argument()]" = None,
):
    """
    Prints out a report per item and per month
    """
    from fruit_store.client import client as grpc_client
    from fruit_store.grpc import factory

    client_ = grpc_client.FruitStoreClient(app_state["host"])

    request = factory.ReportRequestModel()
    report = asyncio.run(client_.request_report(request))

    # TODO: PRETTY PRINT THE REPORT
    print(report)
    return


@app.command()
def healthcheck():
    """
    Pings the server. Exists 1 if there is any error, 0 otherwise
    """
    from fruit_store.client import client as grpc_client

    try:
        client_ = grpc_client.FruitStoreClient(app_state["host"])
        hc = asyncio.run(client_.healthcheck())
        if not hc:
            raise typer.Exit(code=1)
    except Exception as e:
        raise e


if __name__ == "__main__":
    app()
