import datetime as dt
import math
import typing as t

from . import fruit_store_pb2

if t.TYPE_CHECKING:
    from fruit_store.annot.fruit_store.grpc import fruit_store_pb2 as msg_annot


def dt_to_ts(date: "dt.datetime | int") -> int:
    match date:
        case int():
            return date
        case dt.datetime():
            return math.floor(date.timestamp())
    raise TypeError(f"dates must be either int or datetime, not {type(date)}")


def num_to_price(price: "int | float") -> int:
    match price:
        case int():
            return price
        case float():
            return math.ceil(price * 100)
    raise TypeError(f"dates must be either float or int, not {type(price)}")


def sale_event(
    date: "dt.datetime | int", quantity: int, item: str, price: float | int
) -> "msg_annot.SaleEvent":
    ts = dt_to_ts(date)
    price_ = math.ceil(price * 100)  # CONVER CURRENCY TO CENTS.

    return fruit_store_pb2.SaleEvent(  # type: ignore
        date=ts,
        price=price_,
        quantity=quantity,
        item=item,
    )

def report_request(
    date_0: "dt.datetime | int", date_f: "dt.datetime | int",
) -> "msg_annot.ReportRequest":

    return fruit_store_pb2.ReportRequest(  # type: ignore
        date0=dt_to_ts(date_0),
        datef=dt_to_ts(date_f),
    )
