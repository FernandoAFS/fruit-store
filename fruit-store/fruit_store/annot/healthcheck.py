import typing as t

class HealthcheckableProtocol(t.Protocol):
    async def healthcheck(self) -> bool:
        ...
