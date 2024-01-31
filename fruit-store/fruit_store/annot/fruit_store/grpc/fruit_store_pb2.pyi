from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SaleEvent(_message.Message):
    __slots__ = ("date", "quantity", "item", "price")
    DATE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    date: float
    quantity: int
    item: str
    price: int
    def __init__(self, date: _Optional[float] = ..., quantity: _Optional[int] = ..., item: _Optional[str] = ..., price: _Optional[int] = ...) -> None: ...

class SaleReply(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: int
    def __init__(self, code: _Optional[int] = ...) -> None: ...

class ReportRequest(_message.Message):
    __slots__ = ("date0", "datef")
    DATE0_FIELD_NUMBER: _ClassVar[int]
    DATEF_FIELD_NUMBER: _ClassVar[int]
    date0: float
    datef: float
    def __init__(self, date0: _Optional[float] = ..., datef: _Optional[float] = ...) -> None: ...

class ReportResponse(_message.Message):
    __slots__ = ("items",)
    class ItemsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ReportItem
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ReportItem, _Mapping]] = ...) -> None: ...
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.MessageMap[str, ReportItem]
    def __init__(self, items: _Optional[_Mapping[str, ReportItem]] = ...) -> None: ...

class ReportItem(_message.Message):
    __slots__ = ("totalQuantity", "averagePerSale", "totalRevenue", "monthly")
    class MonthlyEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ReportItemMonthly
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ReportItemMonthly, _Mapping]] = ...) -> None: ...
    TOTALQUANTITY_FIELD_NUMBER: _ClassVar[int]
    AVERAGEPERSALE_FIELD_NUMBER: _ClassVar[int]
    TOTALREVENUE_FIELD_NUMBER: _ClassVar[int]
    MONTHLY_FIELD_NUMBER: _ClassVar[int]
    totalQuantity: int
    averagePerSale: int
    totalRevenue: int
    monthly: _containers.MessageMap[str, ReportItemMonthly]
    def __init__(self, totalQuantity: _Optional[int] = ..., averagePerSale: _Optional[int] = ..., totalRevenue: _Optional[int] = ..., monthly: _Optional[_Mapping[str, ReportItemMonthly]] = ...) -> None: ...

class ReportItemMonthly(_message.Message):
    __slots__ = ("totalQuantity", "averagePerSale", "totalRevenue")
    TOTALQUANTITY_FIELD_NUMBER: _ClassVar[int]
    AVERAGEPERSALE_FIELD_NUMBER: _ClassVar[int]
    TOTALREVENUE_FIELD_NUMBER: _ClassVar[int]
    totalQuantity: int
    averagePerSale: int
    totalRevenue: int
    def __init__(self, totalQuantity: _Optional[int] = ..., averagePerSale: _Optional[int] = ..., totalRevenue: _Optional[int] = ...) -> None: ...
