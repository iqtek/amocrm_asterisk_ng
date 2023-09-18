from uuid import UUID

from pydantic import BaseModel


class Secrets(BaseModel):
    client_id: UUID
    access_token: str
    refresh_token: str


class HandleSecretsEndpoint:

    __slots__ = ()

    async def secrets(self, request: Secrets) -> None:
        pass
