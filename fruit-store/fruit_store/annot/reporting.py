import typing as t

if t.TYPE_CHECKING:
    import datetime as dt

ReportDict: t.TypeAlias = "t.Mapping[str, ItemReportDict]"


class ItemReportDict(t.TypedDict):
    total_quantity: int
    average_per_sale: int
    total_revenue: float
    monthly: t.Mapping[str, "ItemMonthlyReportDict"]


class ItemMonthlyReportDict(t.TypedDict):
    total_quantity: int
    average_per_sale: int
    total_revenue: float


class ReportFactoryProtocol(t.Protocol):
    async def generate_report(
        self, date_0: "dt.datetime | None" = None, date_f: "dt.datetime | None" = None
    ) -> "ReportDict":
        ...

    async def healthcheck(self) -> bool:
        ...
