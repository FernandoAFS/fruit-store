import collections
import dataclasses as dtcs
import datetime as dt
import json
import math
import operator as op
import typing as t

from google.protobuf.json_format import MessageToDict

from fruit_store.util import casing

from . import fruit_store_pb2

if t.TYPE_CHECKING:
    from fruit_store.annot import reporting as report_annot
    from fruit_store.annot.fruit_store.grpc import fruit_store_pb2 as msg_annot

T = t.TypeVar("T")


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
class ReportResponseModel:
    report_dict: "report_annot.ReportDict"

    def to_grpc(self) -> "msg_annot.ReportResponse":
        return report_response(self.report_dict)

    @staticmethod
    def from_grpc(resp: "msg_annot.ReportResponse") -> "ReportResponseModel":
        def rec_camel_to_snake(d: "T") -> "T":
            match d:
                # TODO: IMPROVE THIS AND CHECK FOR MAPPING INSTEAD.
                case dict():
                    ks = d.keys()
                    vs = d.values()
                    snake_case: map[str] = map(casing.camel_to_snake, ks)
                    conv_values = map(rec_camel_to_snake, vs)
                    return dict(zip(snake_case, conv_values, strict=False))  # type: ignore

            return d

        resp_d = MessageToDict(resp)
        if len(resp_d) <= 0:
            return ReportResponseModel({})
        d = rec_camel_to_snake(resp_d["items"])
        return ReportResponseModel(report_dict=d)

    def __str__(self) -> str:
        def present_month_report(d: "report_annot.ItemMonthlyReportDict"):
            od = collections.OrderedDict()
            od["total_quantity"] = d["total_quantity"]
            od["average_per_sale"] = d["average_per_sale"]
            od["total_revenue"] = d["total_revenue"]
            return od

        def present_item_report(d: "report_annot.ItemReportDict"):
            od = collections.OrderedDict()
            od["total_quantity"] = d["total_quantity"]
            od["average_per_sale"] = d["average_per_sale"]
            od["total_revenue"] = d["total_revenue"]

            sorted_monthly = sorted(d["monthly"].items(), key=op.itemgetter(0))
            sorted_months = map(op.itemgetter(0), sorted_monthly)
            sorted_month_reports = map(op.itemgetter(1), sorted_monthly)
            sorted_prsented_months = map(present_month_report, sorted_month_reports)

            od["monthly"] = dict(
                zip(sorted_months, sorted_prsented_months, strict=True)
            )

            return od

        items = self.report_dict.keys()
        item_reports = self.report_dict.values()
        present_reports = map(present_item_report, item_reports)

        present_d = dict(zip(items, present_reports, strict=True))
        return json.dumps(present_d, indent=4)


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

        response.items[item].totalRevenue = math.floor(
            item_report["total_revenue"] / 100
        )
        for month, monthly_report in item_report["monthly"].items():
            response.items[item].monthly[month].totalQuantity = monthly_report[
                "total_quantity"
            ]
            response.items[item].monthly[month].averagePerSale = monthly_report[
                "average_per_sale"
            ]
            response.items[item].monthly[month].totalRevenue = math.floor(
                monthly_report["total_revenue"] / 100
            )

    return response
