from typing import Optional

from amocrm_api_client import AmoCrmApiClient
from glassio.dispatcher import IDispatcher
from glassio.initializable_components import AbstractInitializableComponent
from glassio.initializable_components import InitializableComponent

from amocrm_asterisk_ng.domain import IGetResponsibleUserByPhoneQuery
from amocrm_asterisk_ng.domain import IGetUserIdByPhoneQuery

from ..core import IGetPhoneByUserIdQuery
from ..core import IGetUsersEmailAddressesQuery

from .query_handlers import GetPhoneByUserIdQuery
from .query_handlers import GetUserIdByPhoneQuery
from .redirect_to_responsible import GetResponsibleUserByPhoneQuery


__all__ = [
    "AmocrmKernelComponent",
]


class AmocrmKernelComponent(AbstractInitializableComponent):

    __slots__ = (
        "__dispatcher",
        "__amo_client",
        "__raise_card_component",
        "__call_manager_component",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        dispatcher: IDispatcher,
        raise_card_component: InitializableComponent,
        call_manager_component: InitializableComponent,
    ) -> None:
        super().__init__()
        self.__amo_client = amo_client
        self.__dispatcher = dispatcher
        self.__raise_card_component = raise_card_component
        self.__call_manager_component = call_manager_component

    async def _initialize(self) -> None:
        await self.__amo_client.initialize()

        self.__dispatcher.add_function(
            function_type=IGetUserIdByPhoneQuery,
            function=GetUserIdByPhoneQuery(
                amo_client=self.__amo_client,
                get_users_email_addresses=self.__dispatcher.get_function(IGetUsersEmailAddressesQuery),
            )
        )
        self.__dispatcher.add_function(
            function_type=IGetPhoneByUserIdQuery,
            function=GetPhoneByUserIdQuery(
                amo_client=self.__amo_client,
                get_users_email_addresses=self.__dispatcher.get_function(IGetUsersEmailAddressesQuery),
            )
        )

        self.__dispatcher.add_function(
            function_type=IGetResponsibleUserByPhoneQuery,
            function=GetResponsibleUserByPhoneQuery(
                amo_client=self.__amo_client,
                get_phone_by_user_id_query=self.__dispatcher.get_function(IGetPhoneByUserIdQuery),
            )
        )

        await self.__raise_card_component.initialize()
        await self.__call_manager_component.initialize()

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        await self.__call_manager_component.deinitialize()
        await self.__raise_card_component.deinitialize()

        self.__dispatcher.delete_function(IGetResponsibleUserByPhoneQuery)
        self.__dispatcher.delete_function(IGetUserIdByPhoneQuery)
        self.__dispatcher.delete_function(IGetPhoneByUserIdQuery)

        await self.__amo_client.deinitialize()
