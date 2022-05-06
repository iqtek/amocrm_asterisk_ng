from fastapi import FastAPI

from amocrm_asterisk_ng.domain import IGetResponsibleUserByPhoneQuery
from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import InitializableComponent

from .RedirectToResponsibleView import RedirectToResponsibleView


__all__ = [
    "RedirectToResponsibleComponent",
]


class RedirectToResponsibleComponent(InitializableComponent):

    __slots__ = (
        "__app",
        "__dispatcher",
    )

    def __init__(
        self,
        app: FastAPI,
        dispatcher: IDispatcher,
    ) -> None:
        self.__app = app
        self.__dispatcher = dispatcher

    async def initialize(self) -> None:
        view = RedirectToResponsibleView(
            get_responsible_user_by_phone_query=self.__dispatcher.get_function(IGetResponsibleUserByPhoneQuery)
        )

        self.__app.add_api_route(
            path="/amocrm/responsible",
            endpoint=view.handle,
            methods=["GET"],
        )

    async def deinitialize(self) -> None:
        pass
