from typing import Optional

from amocrm_api_client import AmoCrmApiClient
from glassio.dispatcher import IDispatcher
from glassio.initializable_components import AbstractInitializableComponent
from glassio.initializable_components import InitializableComponent

from amocrm_asterisk_ng.domain import IGetResponsibleOperatorByPhoneQuery
from amocrm_asterisk_ng.domain import IGetOperatorIdByPhoneQuery

from ..core import IGetPhoneByOperatorIdQuery
from ..core import IGetOperatorsEmailAddressesQuery

from .query_handlers import GetPhoneByOperatorIdQuery
from .query_handlers import GetOperatorIdByPhoneQuery
from .redirect_to_responsible import GetResponsibleOperatorByPhoneQuery


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
            function_type=IGetOperatorIdByPhoneQuery,
            function=GetOperatorIdByPhoneQuery(
                amo_client=self.__amo_client,
                get_users_email_addresses=self.__dispatcher.get_function(IGetOperatorsEmailAddressesQuery),
            )
        )
        self.__dispatcher.add_function(
            function_type=IGetPhoneByOperatorIdQuery,
            function=GetPhoneByOperatorIdQuery(
                amo_client=self.__amo_client,
                get_users_email_addresses=self.__dispatcher.get_function(IGetOperatorsEmailAddressesQuery),
            )
        )

        self.__dispatcher.add_function(
            function_type=IGetResponsibleOperatorByPhoneQuery,
            function=GetResponsibleOperatorByPhoneQuery(
                amo_client=self.__amo_client,
                get_phone_by_user_id_query=self.__dispatcher.get_function(IGetPhoneByOperatorIdQuery),
            )
        )

        await self.__raise_card_component.initialize()
        await self.__call_manager_component.initialize()

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        await self.__call_manager_component.deinitialize()
        await self.__raise_card_component.deinitialize()

        self.__dispatcher.delete_function(IGetResponsibleOperatorByPhoneQuery)
        self.__dispatcher.delete_function(IGetOperatorIdByPhoneQuery)
        self.__dispatcher.delete_function(IGetPhoneByOperatorIdQuery)

        await self.__amo_client.deinitialize()
