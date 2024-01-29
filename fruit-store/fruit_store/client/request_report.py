
import asyncio
import logging
import grpc

from fruit_store.grpc import fruit_store_pb2, fruit_store_pb2_grpc

async def test_request() -> None:
    # MOVE TO
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = fruit_store_pb2_grpc.ServerStub(channel)
        response = await stub.PutSale(fruit_store_pb2.SaleEvent(
            date=10001,
            quantity=1,
            item="papaya",
            price=125
        ))
    print(type(response))


