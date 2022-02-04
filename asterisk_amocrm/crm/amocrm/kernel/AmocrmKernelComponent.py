from asterisk_amocrm.infrastructure import (
    IComponent,
    IDispatcher,
)
from .query_handlers import (
    IGetUserIdByPhoneQH,
    GetUserIdByPhoneQH,
)
from amo_crm_api_client import AmoCrmApiClient
from ..core import GetUserIdByPhoneQuery


__all__ = [
    "AmocrmKernelComponent",
]


class AmocrmKernelComponent(IComponent):

    def __init__(
        self,
        dispatcher: IDispatcher,
        amo_client: AmoCrmApiClient,
        raise_card_component: IComponent,
        call_manager_component: IComponent,
    ) -> None:
        self.__dispatcher = dispatcher
        self.__amo_client = amo_client
        self.__raise_card_component = raise_card_component
        self.__call_manager_component = call_manager_component

    async def initialize(self) -> None:
        await self.__amo_client.initialize()

        await self.__dispatcher.attach_query_handler(
            IGetUserIdByPhoneQH,
            GetUserIdByPhoneQH(
                amo_client=self.__amo_client,
                dispatcher=self.__dispatcher,
            )
        )

        await self.__raise_card_component.initialize()
        await self.__call_manager_component.initialize()

    async def deinitialize(self) -> None:
        await self.__call_manager_component.deinitialize()
        await self.__raise_card_component.deinitialize()

        await self.__dispatcher.detach_query_handler(
            GetUserIdByPhoneQH,
        )
        await self.__amo_client.deinitialize()
