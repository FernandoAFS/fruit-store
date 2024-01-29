import typing as t

from fruit_store.grpc import fruit_store_pb2, fruit_store_pb2_grpc

if t.TYPE_CHECKING:
    import grpc

    from fruit_store.annot.fruit_store.grpc import (
        fruit_store_pb2 as msg_annot,
    )


class FrutStoreServer(fruit_store_pb2_grpc.ServerServicer):
    async def PutSale(
        self, request: "msg_annot.SaleEvent", context: "grpc.RpcContext"
    ) -> "msg_annot.Empty":
        raise NotImplementedError("Wait for data storage implementation")
        return fruit_store_pb2.Empty()  # type: ignore

    async def GetReport(
        self, request: "msg_annot.ReportRequest", context: "grpc.RpcContext"
    ) -> "msg_annot.ReportResponse":
        raise NotImplementedError("Wait for data-calc implementation")

    async def Healthcheck(
        self, request: "msg_annot.Empty", context: "grpc.RpcContext"
    ) -> "msg_annot.Empty":
        # TODO: IMPROVE. CHECK ON CALC AND STORE BACKENDS
        return fruit_store_pb2.Empty()  # type: ignore
