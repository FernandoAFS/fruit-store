import typing as t

if t.TYPE_CHECKING:
    import datetime as dt


class PurchraseEventProtocol(t.Protocol):
    "Basic event model. Typically recieved in JSON format"

    @property
    def date(self) -> "dt.datetime":
        ...

    @property
    def item(self) -> str:
        ...

    @property
    def quantity(self) -> int:
        ...

    @property
    def price(self) -> int:
        ...


class PurchraseCollectorProtocol(t.Protocol):
    """Event collector. Recieves purchrase events and keeps them for future
    calculations"""

    async def put_purchrase_event(self, event: "PurchraseEventProtocol") -> None:
        ...

    async def healthcheck(self) -> bool:
        ...

class PurchraseCollectorFactoryProtocol(t.Protocol):
    """Factory of savers. Typically used for config items"""

    def purchrase_collector_protocol(self) -> "PurchraseCollectorProtocol":
        ...
