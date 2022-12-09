from typing import Any
from typing import Mapping
from typing import Optional

from amocrm_api_client import AmoCrmApiClient
from amocrm_api_client import AmoCrmApiClientConfig
from amocrm_api_client import create_amocrm_api_client

from amocrm_api_client.token_provider import StandardTokenProviderFactory

from asterisk_ng.system.container import Key
from asterisk_ng.system.container import SingletonResolver
from asterisk_ng.system.container import container

from asterisk_ng.system.plugin import IPlugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface


__all__ = ["AmoClientPlugin"]


class AmoClientPlugin(IPlugin):

    __slots__ = (
        "__amo_client"
    )

    def __init__(self) -> None:
        super().__init__()
        self.__amo_client: Optional[AmoCrmApiClient] = None

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            exported=Interface(
                container=[Key(AmoCrmApiClient)],
            )
        )

    def __client_factory(self, settings: Mapping[str, Any]) -> AmoCrmApiClient:
        token_provider_factory = StandardTokenProviderFactory()

        token_provider = token_provider_factory.get_instance(settings=settings)

        return create_amocrm_api_client(
            config=AmoCrmApiClientConfig(base_url=settings["base_url"]),
            token_provider=token_provider,
        )

    async def upload(self, settings: Mapping[str, Any]) -> None:
        self.__amo_client = self.__client_factory(settings)
        await self.__amo_client.initialize()
        container.set_resolver(Key(AmoCrmApiClient), SingletonResolver(self.__amo_client))

    async def reload(self, settings: Mapping[str, Any]) -> None:
        new_amo_client = self.__client_factory(settings)
        await self.__amo_client.deinitialize()
        self.__amo_client = new_amo_client
        container.set_resolver(Key(AmoCrmApiClient), SingletonResolver(self.__amo_client))

    async def unload(self) -> None:
        container.delete_resolver(Key(AmoCrmApiClient))
        await self.__amo_client.deinitialize()
