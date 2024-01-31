import collections
import dataclasses as dtcs
import datetime as dt
import json
import operator as op
import typing as t

import pendulum as pend
from google.protobuf.json_format import MessageToDict

from fruit_store.environment import constants as ct
from fruit_store.util import casing

from . import fruit_store_pb2

if t.TYPE_CHECKING:
    from fruit_store.annot import reporting as report_annot
    from fruit_store.annot.fruit_store.grpc import fruit_store_pb2 as msg_annot

T = t.TypeVar("T")


class CustomGrpcSerializationError(TypeError):
    ...


class SaleEventQuantityError(CustomGrpcSerializationError):
    ...


class SaleEventPriceError(CustomGrpcSerializationError):
    ...


class DateTooHighError(CustomGrpcSerializationError):
    ...


class DateTooLowError(CustomGrpcSerializationError):
    ...


MIN_DATE = pend.datetime(year=1970, month=1, day=1)
MAX_DATE = pend.datetime(year=2242, month=12, day=30)

MAX_PRICE = (2**32 - 1) // ct.PRICE_DECIMALS
MIN_PRICE = 0

MAX_QUANTITY = 2**32 - 1
MIN_QUANTITY = 0


def dt_to_ts(date: "dt.datetime | pend.DateTime | float") -> float:
    "Returns positive timestamp in miliseconds given a datetime. Assuming"
    match date:
        case float():
            ts = date
        case dt.datetime():
            ts = pend.instance(date).timestamp()
        case pend.DateTime():
            ts = date.timestamp()
        case _:
            raise TypeError(f"dates must be either float or datetime, not {type(date)}")

    return ts


def ts_to_dt(date: "dt.datetime | pend.DateTime | float") -> "pend.DateTime":
    ""
    match date:
        case float():
            dt_ = pend.from_timestamp(date)
        case pend.DateTime():
            dt_ = date
        case dt.datetime():
            dt_ = pend.instance(date)
        case _:
            raise TypeError(f"dates must be either float or datetime, not {type(date)}")

    if dt_ > MAX_DATE:
        raise DateTooHighError("Date should be below: f{MAX_DATE}")

    if dt_ < MIN_DATE:
        raise DateTooLowError("Date should be above: f{MIN_DATE}")

    return dt_


def num_to_price(num: float | int) -> int:
    match num:
        case int():
            return num
        case float():
            return int(num * ct.PRICE_DECIMALS)

    raise TypeError("num must be either float or int")


def price_to_num(price: int) -> float:
    return price / ct.PRICE_DECIMALS


@dtcs.dataclass(frozen=True)
class ReportResponseModel:
    report_dict: "report_annot.ReportDict"

    def to_grpc(self) -> "msg_annot.ReportResponse":
        response: "msg_annot.ReportResponse" = fruit_store_pb2.ReportResponse()  # type: ignore

        for item, item_report in self.report_dict.items():
            response.items[item].totalQuantity = item_report["total_quantity"]
            response.items[item].averagePerSale = item_report["average_per_sale"]

            response.items[item].totalRevenue = item_report["total_revenue"]

            for month, monthly_report in item_report["monthly"].items():
                response.items[item].monthly[month].totalQuantity = monthly_report[
                    "total_quantity"
                ]
                response.items[item].monthly[month].averagePerSale = monthly_report[
                    "average_per_sale"
                ]
                response.items[item].monthly[month].totalRevenue = monthly_report[
                    "total_revenue"
                ]
        return response

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
            od["total_revenue"] = int(d["total_revenue"] / ct.PRICE_DECIMALS)
            return od

        def present_item_report(d: "report_annot.ItemReportDict"):
            od = collections.OrderedDict()
            od["total_quantity"] = d["total_quantity"]
            od["average_per_sale"] = d["average_per_sale"]
            od["total_revenue"] = int(d["total_revenue"] / ct.PRICE_DECIMALS)

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
    date0: "pend.DateTime | dt.datetime | None" = None
    datef: "pend.DateTime | dt.datetime | None" = None

    def to_grpc(self) -> "msg_annot.ReportRequest":
        return report_request(self.date0, self.datef)

    @staticmethod
    def from_grpc(ev: "msg_annot.ReportRequest") -> "ReportRequestModel":
        d0 = pend.from_timestamp(ev.date0)
        df = pend.from_timestamp(ev.datef)
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

    date: "pend.DateTime"
    item: str
    quantity: int
    price: int

    def to_grpc(self) -> "msg_annot.SaleEvent":
        if self.quantity <= MIN_QUANTITY:
            raise SaleEventQuantityError("Sale event quantity must always be above 0")
        if self.price <= MIN_PRICE:
            raise SaleEventPriceError("Sale event price must always be above 0")

        if self.quantity >= MAX_QUANTITY:
            raise SaleEventQuantityError(
                "Sale event quantity must always be below f{MAX_QUANTITY}"
            )
        if self.price >= MAX_PRICE:
            raise SaleEventPriceError(
                "Sale event quantity must always be below f{MAX_PRICE}"
            )

        ts = dt_to_ts(self.date)
        price_ = int(self.price * ct.PRICE_DECIMALS)  # CONVER CURRENCY TO CENTS.

        return fruit_store_pb2.SaleEvent(  # type: ignore
            date=ts,
            price=price_,
            quantity=int(self.quantity),
            item=self.item,
        )

    @staticmethod
    def from_grpc(ev: "msg_annot.SaleEvent") -> "PurchaseEventModel":
        d_ = ts_to_dt(ev.date)
        return PurchaseEventModel(
            date=d_,
            item=ev.item,
            quantity=ev.quantity,
            price=ev.price,
        )

    @staticmethod
    def from_dict(d: "t.Mapping[str, t.Any]") -> "PurchaseEventModel":
        return PurchaseEventModel(
            **d,
        )


def report_request(
    date_0: "dt.datetime | pend.DateTime | float | None",
    date_f: "dt.datetime | pend.DateTime | float | None",
) -> "msg_annot.ReportRequest":
    d = {}
    if date_0 is not None:
        d["date0"] = dt_to_ts(date_0)
    if date_f is not None:
        d["datef"] = dt_to_ts(date_f)

    return fruit_store_pb2.ReportRequest(**d)  # type: ignore
