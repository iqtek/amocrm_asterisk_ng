from typing import Any
from typing import Mapping
from typing import Optional

from logging import Logger

from amocrm_api_client import AmoCrmApiClient
from amocrm_api_client import AmoCrmApiClientConfig
from amocrm_api_client import create_amocrm_api_client

from amocrm_api_client.token_provider import StandardTokenProviderFactory

from fastapi import FastAPI

from asterisk_ng.system.container import Key
from asterisk_ng.system.container import SingletonResolver
from asterisk_ng.system.container import container

from asterisk_ng.system.plugin import Plugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface

from ..helper import generate_auth_url_for_authorizer

__all__ = ["ViaAuthorizerTokenProviderPlugin.py"]


class ViaAuthorizerTokenProviderPlugin(Plugin):

    __slots__ = (
        "__amo_client"
    )

    def __init__(self) -> None:
        super().__init__()
        self.__amo_client: Optional[AmoCrmApiClient] = None

    def __client_factory(self, settings: Mapping[str, Any]) -> AmoCrmApiClient:

        async def get_tokens():
            auth_url = generate_auth_url_for_authorizer()

        async def refresh_tokens(refresh_token: str):
            pass

        class Tokens(BaseModel):
            client_id: UUID
            access_token: str
            refresh_token: str

        async def handle_tokens(request: Tokens) -> None:
            pass

        token_provider_factory = StandardTokenProviderFactory()

        token_provider = token_provider_factory.get_instance(settings=settings)

        return create_amocrm_api_client(
            config=AmoCrmApiClientConfig(base_url=settings["base_url"]),
            token_provider=token_provider,
        )

    async def upload(self, settings: Mapping[str, Any]) -> None:
        app = container.resolve(Key(FastAPI))
        logger = container.resolve(Key(Logger))

        self.__amo_client = self.__client_factory(settings)
        await self.__amo_client.initialize()

        try:
            _ = await self.__amo_client.account.get_info()
        except ValueError:
            pass

        container.set_resolver(Key(AmoCrmApiClient), SingletonResolver(self.__amo_client))

    async def reload(self, settings: Mapping[str, Any]) -> None:
        new_amo_client = self.__client_factory(settings)
        await self.__amo_client.deinitialize()
        self.__amo_client = new_amo_client
        container.set_resolver(Key(AmoCrmApiClient), SingletonResolver(self.__amo_client))

    async def unload(self) -> None:
        container.delete_resolver(Key(AmoCrmApiClient))
        await self.__amo_client.deinitialize()
