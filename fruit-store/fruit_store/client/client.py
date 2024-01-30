import dataclasses as dtcs
import datetime as dt
import typing as t

import grpc

from fruit_store.grpc import (
    factory as protobuf_factory,
)
from fruit_store.grpc import (
    fruit_store_pb2,
    fruit_store_pb2_grpc,
)

if t.TYPE_CHECKING:
    from fruit_store.annot.fruit_store.grpc import fruit_store_pb2 as msg_annot


# TODO: INCLUDE
@dtcs.dataclass(frozen=True)
class FruitStoreClient:
    host: str

    async def put_sale(
        self, date: "dt.datetime | int", quantity: int, item: str, price: float | int
    ) -> None:
        sale = protobuf_factory.sale_event(date, quantity, item, price)
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = fruit_store_pb2_grpc.ServerStub(channel)
            await stub.PutSale(sale)
        return

    async def request_report(
        self, date_0: "dt.datetime", date_f: "dt.datetime"
    ) -> "msg_annot.ReportResponse":
        report_request = protobuf_factory.report_request(date_0, date_f)
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = fruit_store_pb2_grpc.ServerStub(channel)
            response = await stub.PutSale(report_request)
        return response

    # TODO: IMPROVE ON RETURN TYPE
    async def healthcheck(self) -> bool:
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = fruit_store_pb2_grpc.ServerStub(channel)
            await stub.Healthcheck(fruit_store_pb2.Empty())
        return True

def default_fruit_store_client_factory(host: str):
    ...
