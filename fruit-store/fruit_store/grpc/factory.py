import dataclasses as dtcs
import datetime as dt
import math
import typing as t

from . import fruit_store_pb2

if t.TYPE_CHECKING:
    from fruit_store.annot import reporting as report_annot
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


@dtcs.dataclass(frozen=True)
class ReportRequestModel:
    date0: "dt.datetime | None" = None
    datef: "dt.datetime | None" = None

    def to_grpc(self) -> "msg_annot.ReportRequest":
        return report_request(self.date0, self.datef)

    @staticmethod
    def from_grpc(ev: "msg_annot.ReportRequest") -> "ReportRequestModel":
        d0 = dt.datetime.fromtimestamp(ev.date0)
        df = dt.datetime.fromtimestamp(ev.datef)
        return ReportRequestModel(
            date0=d0,
            datef=df,
        )


@dtcs.dataclass(frozen=True)
class PurchaseEventModel:
    """
    Class that complies with the purchase event protocol and encapsulates
    methods to generate grpc classes
    """

    date: "dt.datetime"
    item: str
    quantity: int
    price: int

    def to_grpc(self) -> "msg_annot.SaleEvent":
        return sale_event(self.date, self.quantity, self.item, self.price)

    @staticmethod
    def from_grpc(ev: "msg_annot.SaleEvent") -> "PurchaseEventModel":
        d_ = dt.datetime.fromtimestamp(ev.date)
        return PurchaseEventModel(
            date=d_,
            item=ev.item,
            quantity=ev.quantity,
            price=ev.price,
        )

    @staticmethod
    def from_dict(d: "t.Mapping[str, t.Any]") -> "PurchaseEventModel":
        return PurchaseEventModel(**d)


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
    date_0: "dt.datetime | int | None",
    date_f: "dt.datetime | int | None",
) -> "msg_annot.ReportRequest":
    d = {}
    if date_0 is not None:
        d["date0"] = dt_to_ts(date_0)
    if date_f is not None:
        d["datef"] = dt_to_ts(date_f)

    return fruit_store_pb2.ReportRequest(**d)  # type: ignore


def report_response(d: "report_annot.ReportDict") -> "msg_annot.ReportResponse":
    response: "msg_annot.ReportResponse" = fruit_store_pb2.ReportResponse()  # type: ignore

    for item, item_report in d.items():
        response.items[item].totalQuantity = item_report["total_quantity"]
        response.items[item].averagePerSale = item_report["average_per_sale"]
        response.items[item].totalRevenue = math.floor(item_report["total_revenue"])
        for month, monthly_report in item_report["monthly_results"].items():
            response.items[item].monthly[month].totalQuantity = monthly_report[
                "total_quantity"
            ]
            response.items[item].monthly[month].averagePerSale = monthly_report[
                "average_per_sale"
            ]
            response.items[item].monthly[month].totalRevenue = math.floor(
                monthly_report["total_revenue"]
            )

    return response
