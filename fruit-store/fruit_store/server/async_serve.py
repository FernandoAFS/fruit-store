import logging

import grpc

from fruit_store.grpc import fruit_store_pb2_grpc

from . import server as fruit_server

LISTEN_ADDR = "[::]:50051"


async def serve() -> None:
    server = grpc.aio.server()
    fruit_store_pb2_grpc.add_ServerServicer_to_server(
        fruit_server.FrutStoreServer(), server
    )
    server.add_insecure_port(LISTEN_ADDR)
    logging.info("Starting server on %s", LISTEN_ADDR)
    # TODO: IMPROVE ON TERMINATION
    await server.start()
    await server.wait_for_termination()

