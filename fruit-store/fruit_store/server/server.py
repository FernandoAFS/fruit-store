import asyncio
import dataclasses as dtcs
import typing as t

from fruit_store.grpc import (
    factory as grpc_factory,
)
from fruit_store.grpc import (
    fruit_store_pb2,
    fruit_store_pb2_grpc,
)

if t.TYPE_CHECKING:
    import grpc

    from fruit_store.annot import (
        data_input as di_annot,
    )
    from fruit_store.annot import (
        reporting as report_annot,
    )
    from fruit_store.annot.fruit_store.grpc import (
        fruit_store_pb2 as msg_annot,
    )


@dtcs.dataclass(frozen=True)
class FrutStoreServer(fruit_store_pb2_grpc.ServerServicer):
    data_collector: "di_annot.PurchraseCollectorProtocol"
    report_generator: "report_annot.ReportFactoryProtocol"

    async def PutSale(
        self, request: "msg_annot.SaleEvent", context: "grpc.RpcContext"
    ) -> "msg_annot.Empty":
        event = grpc_factory.PurchaseEventModel.from_grpc(request)
        await self.data_collector.put_purchrase_event(event)
        return fruit_store_pb2.Empty()  # type: ignore

    async def GetReport(
        self, request: "msg_annot.ReportRequest", context: "grpc.RpcContext"
    ) -> "msg_annot.ReportResponse":
        items = await self.report_generator.generate_report(
            request.date0, request.date0
        )
        items_wrapper = grpc_factory.ReportResponseModel(items)
        grpc_response = items_wrapper.to_grpc()
        return grpc_response

    async def Healthcheck(
        self, request: "msg_annot.Empty", context: "grpc.RpcContext"
    ) -> "msg_annot.Empty":
        # TODO: IMPROVE. CHECK ON CALC AND STORE BACKENDS
        hcs = await asyncio.gather(
            self.data_collector.healthcheck(),
            self.report_generator.healthcheck(),
        )

        if not all(hcs):
            raise Exception("Healthcheck failed")

        return fruit_store_pb2.Empty()  # type: ignore


def default_frut_store_server() -> "FrutStoreServer":
    from fruit_store.mem_storage import mem_storage

    m_ = mem_storage.MemoryStorage()
    return FrutStoreServer(
        data_collector=m_,
        report_generator=m_,
    )
