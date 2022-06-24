from fastapi import FastAPI

from glassio.dispatcher import IDispatcher
from glassio.initializable_components import AbstractInitializableComponent

from amocrm_asterisk_ng.domain import IGetResponsibleOperatorByPhoneQuery

from .RedirectToResponsibleView import RedirectToResponsibleView


__all__ = [
    "RedirectToResponsibleComponent",
]


class RedirectToResponsibleComponent(AbstractInitializableComponent):

    __slots__ = (
        "__app",
        "__dispatcher",
    )

    def __init__(
        self,
        app: FastAPI,
        dispatcher: IDispatcher,
    ) -> None:
        super().__init__()
        self.__app = app
        self.__dispatcher = dispatcher

    async def _initialize(self) -> None:
        view = RedirectToResponsibleView(
            get_responsible_user_by_phone_query=self.__dispatcher.get_function(IGetResponsibleOperatorByPhoneQuery)
        )

        self.__app.add_api_route(
            path="/amocrm/responsible",
            endpoint=view.handle,
            methods=["GET"],
        )
