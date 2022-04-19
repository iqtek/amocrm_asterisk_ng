from fastapi import FastAPI

from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import InitializableComponent

from ...core import IGetUsersEmailAddressesQuery
from .AsteriskWidgetConfig import AsteriskWidgetConfig
from .GetUsersEmailAddressesQuery import GetUsersEmailAddressesQuery
from .WidgetView import WidgetView


__all__ = [
    "AsteriskWidgetComponent",
]


class AsteriskWidgetComponent(InitializableComponent):

    __slots__ = (
        "__config",
        "__app",
        "__dispatcher",
        "__widget_view",
    )

    def __init__(
        self,
        config: AsteriskWidgetConfig,
        app: FastAPI,
        dispatcher: IDispatcher,
        widget_view: WidgetView,
    ) -> None:
        self.__config = config
        self.__app = app
        self.__dispatcher = dispatcher
        self.__widget_view = widget_view

    async def initialize(self) -> None:

        self.__app.add_route(
            "/amocrm/calls",
            self.__widget_view.handle,
            methods=["GET"]
        )

        self.__dispatcher.add_function(
            function_type=IGetUsersEmailAddressesQuery,
            function=GetUsersEmailAddressesQuery(
                users=self.__config.users,
            )
        )

    async def deinitialize(self) -> None:

        self.__app.routes.remove(widget_view)

        self.__dispatcher.delete_function(
            function_type=IGetUsersEmailAddressesQuery,
        )
