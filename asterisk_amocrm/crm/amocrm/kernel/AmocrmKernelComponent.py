from amo_crm_api_client import AmoCrmApiClient

from asterisk_amocrm.infrastructure import InitializableComponent
from asterisk_amocrm.infrastructure import IDispatcher

from ..core import IGetUserIdByPhoneQuery
from ..core import IGetUserEmailByPhoneQuery
from .query_handlers import GetUserIdByPhoneQuery


__all__ = [
    "AmocrmKernelComponent",
]


class AmocrmKernelComponent(InitializableComponent):

    __slots__ = (
        "__dispatcher",
        "__amo_client",
        "__raise_card_component",
        "__call_manager_component",
        "__get_user_id_by_phone_query",
        "__get_user_email_by_phone_query",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        dispatcher: IDispatcher,
        raise_card_component: InitializableComponent,
        call_manager_component: InitializableComponent,
        get_user_id_by_phone_query: IGetUserIdByPhoneQuery,
        get_user_email_by_phone_query: IGetUserEmailByPhoneQuery,
    ) -> None:
        self.__amo_client = amo_client
        self.__dispatcher = dispatcher
        self.__raise_card_component = raise_card_component
        self.__call_manager_component = call_manager_component
        self.__get_user_id_by_phone_query = get_user_id_by_phone_query
        self.__get_user_email_by_phone_query = get_user_email_by_phone_query

    async def initialize(self) -> None:
        await self.__amo_client.initialize()

        self.__dispatcher.add_function(
            function_type=IGetUserIdByPhoneQuery,
            function=GetUserIdByPhoneQuery(
                amo_client=self.__amo_client,
                get_user_email_by_phone_query=self.__get_user_email_by_phone_query,
            )
        )

        await self.__raise_card_component.initialize()
        await self.__call_manager_component.initialize()

    async def deinitialize(self) -> None:
        await self.__call_manager_component.deinitialize()
        await self.__raise_card_component.deinitialize()

        self.__dispatcher.delete_function(
            IGetUserIdByPhoneQuery,
        )
        await self.__amo_client.deinitialize()
