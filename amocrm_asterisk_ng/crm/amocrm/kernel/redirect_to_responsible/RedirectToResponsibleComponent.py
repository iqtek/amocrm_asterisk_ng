from amo_crm_api_client import AmoCrmApiClient

from fastapi import FastAPI

from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import InitializableComponent
from .queries import GetResponsibleUserByPhoneQuery
from .queries import IGetResponsibleUserByPhoneQuery
from .views import RedirectToResponsibleView
from ...core import IGetPhoneByUserIdQuery


__all__ = [
    "RedirectToResponsibleComponent",
]


class RedirectToResponsibleComponent(InitializableComponent):

    __slots__ = (
        "__app",
        "__amo_client",
        "__dispatcher",
    )

    def __init__(
        self,
        app: FastAPI,
        amo_client: AmoCrmApiClient,
        dispatcher: IDispatcher,
    ) -> None:
        self.__app = app
        self.__amo_client = amo_client
        self.__dispatcher = dispatcher

    async def initialize(self) -> None:

        self.__dispatcher.add_function(
            function_type=IGetResponsibleUserByPhoneQuery,
            function=GetResponsibleUserByPhoneQuery(
                amo_client=self.__amo_client,
                get_phone_by_user_id_query=self.__dispatcher.get_function(IGetPhoneByUserIdQuery)
            )
        )

        view = RedirectToResponsibleView(
            get_responsible_user_by_phone_query=self.__dispatcher.get_function(IGetResponsibleUserByPhoneQuery)
        )

        self.__app.add_api_route(
            path="/amocrm/responsible",
            endpoint=view.handle,
            methods=["GET"],
        )

    async def deinitialize(self) -> None:

        self.__dispatcher.delete_function(
            IGetResponsibleUserByPhoneQuery,
        )
