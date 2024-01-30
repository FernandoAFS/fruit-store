
import dataclasses as dtcs


@dtcs.dataclass(frozen=True)
class ServerSettings:
    db: "DbSettings"
    ...


@dtcs.dataclass(frozen=True)
class GrpcClient:
    uri: str

@dtcs.dataclass(frozen=True)
class GrpcServer:
    uri: str


@dtcs.dataclass(frozen=True)
class DbSettings:
    uri: str
    check_same_thread: bool

