import logging

import grpc

from fruit_store.grpc import fruit_store_pb2_grpc

from . import server as fruit_server


async def serve(addr: str) -> None:
    server = grpc.aio.server()
    fruit_store_pb2_grpc.add_ServerServicer_to_server(
        fruit_server.default_frut_store_server(), server
    )
    server.add_insecure_port(addr)
    logging.info("Starting server on %s", addr)
    # TODO: IMPROVE ON TERMINATION
    await server.start()
    await server.wait_for_termination()

