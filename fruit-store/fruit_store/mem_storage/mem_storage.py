"Memory storage of events. Intended for tiny developments or testing"

import collections as col
import dataclasses as dtcs
import logging
import operator as op
import typing as t

if t.TYPE_CHECKING:
    import datetime as dt

    from fruit_store.annot import (
        data_input as di_annot,
    )
    from fruit_store.annot import (
        reporting as report_annot,
    )

logger = logging.getLogger(__name__)



@dtcs.dataclass
class MemMonthItemReporting:
    quantity: int = 0
    sales: int = 0
    revenue: int = 0

    def __add__(
        self, other: "di_annot.PurchraseEventProtocol"
    ) -> "MemMonthItemReporting":
        income = other.price * other.quantity
        return MemMonthItemReporting(
            quantity=self.quantity + other.quantity,
            sales=self.sales + 1,
            revenue=self.revenue + income,
        )

    def to_month_report(self) -> "report_annot.ItemMonthlyReportDict":
        return {
            "total_quantity": self.quantity,
            "average_per_sale": self.quantity // self.sales,  # TO FORCE INT
            "total_revenue": self.revenue,
        }


def item_report(
    data: t.Mapping["dt.datetime", "MemMonthItemReporting"],
    date_0: "dt.datetime | None" = None,
    date_f: "dt.datetime | None" = None,
) -> "report_annot.ItemReportDict":
    if date_0 is not None:
        logger.warning("date_0 informed but not supported. Not used")

    if date_f is not None:
        logger.warning("date_0 informed but not supported. Not used")

    # 1. Accumulate values
    vs = data.values()
    total_quantity: int = sum(map(op.attrgetter("quantity"), vs))
    total_sales: int = sum(map(op.attrgetter("sales"), vs))
    total_revenue: int = sum(map(op.attrgetter("revenue"), vs))
    average_per_sale: int = total_quantity // total_sales

    # 2. Monthly values
    dates_str = map(lambda d: d.strftime("%Y-%m"), data.keys())
    monthly_reports = map(MemMonthItemReporting.to_month_report, vs)

    return {
        "total_quantity": total_quantity,
        "average_per_sale": average_per_sale,
        "total_revenue": total_revenue,
        "monthly": dict(zip(dates_str, monthly_reports, strict=True)),
    }


def default_dict_factory():
    return col.defaultdict(lambda: col.defaultdict(MemMonthItemReporting))


@dtcs.dataclass
class MemoryStorage:
    """Event collector. Recieves purchrase events and keeps them for future
    calculations"""

    accum_: t.MutableMapping[
        str, t.MutableMapping["dt.datetime", "MemMonthItemReporting"]
    ] = dtcs.field(default_factory=default_dict_factory)  # type: ignore

    async def put_purchrase_event(
        self, event: "di_annot.PurchraseEventProtocol"
    ) -> None:
        month = event.date.replace(
            tzinfo=None, day=1, hour=0, minute=0, second=0, microsecond=0
        )
        self.accum_[event.item][month] += event
        return None

    async def generate_report(
        self, date_0: "dt.datetime | None" = None, date_f: "dt.datetime | None" = None
    ) -> "report_annot.ReportDict":
        # TODO: INCLUDE DATE FILTERING
        items = self.accum_.keys()
        item_reports = map(item_report, self.accum_.values())

        return dict(zip(items, item_reports, strict=True))

    async def healthcheck(self) -> bool:
        return True
