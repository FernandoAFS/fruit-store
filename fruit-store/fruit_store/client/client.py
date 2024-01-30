import dataclasses as dtcs
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


@dtcs.dataclass(frozen=True)
class FruitStoreClient:
    host: str

    async def put_sale(self, event: "protobuf_factory.PurchaseEventModel") -> None:
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = fruit_store_pb2_grpc.ServerStub(channel)
            await stub.PutSale(event.to_grpc())
        return

    async def request_report(
        self,
        request: "protobuf_factory.ReportRequestModel",
    ) -> "msg_annot.ReportResponse":
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = fruit_store_pb2_grpc.ServerStub(channel)
            response = await stub.GetReport(request.to_grpc())
        return response

    # TODO: IMPROVE ON RETURN TYPE
    async def healthcheck(self) -> bool:
        async with grpc.aio.insecure_channel(self.host) as channel:
            stub = fruit_store_pb2_grpc.ServerStub(channel)
            await stub.Healthcheck(fruit_store_pb2.Empty())
        return True
