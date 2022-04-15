from fastapi import FastAPI

from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import InitializableComponent

from .AsteriskWidgetConfig import AsteriskWidgetConfig
from .query_handlers import GetUserEmailByPhoneQuery
from .query_handlers import GetUsersEmailAddresses
from .views import WidgetView
from ...core import IGetUserEmailByPhoneQuery
from ...core import IGetUsersEmailAddresses


__all__ = [
    "AsteriskWidgetComponent",
]


class AsteriskWidgetComponent(InitializableComponent):

    __slots__ = (
        "__config",
        "__app",
        "__dispatcher",
        "__widget_view",
        "__logger",
    )

    def __init__(
        self,
        config: AsteriskWidgetConfig,
        app: FastAPI,
        dispatcher: IDispatcher,
        widget_view: WidgetView,
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__app = app
        self.__dispatcher = dispatcher
        self.__widget_view = widget_view
        self.__logger = logger

    async def initialize(self) -> None:

        self.__app.add_route(
            "/amocrm/calls",
            self.__origination_view.handle,
            methods=["GET"]
        )

        self.__dispatcher.add_function(
            function_type=IGetUserEmailByPhoneQuery,
            function=GetUserEmailByPhoneQuery(
                users=self.__config.users,
            )
        )

        self.__dispatcher.add_function(
            function_type=IGetUsersEmailAddresses,
            function=GetUsersEmailAddresses(
                users=self.__config.users,
            )
        )

    async def deinitialize(self) -> None:

        self.__app.routes.remove(widget_view)

        self.__dispatcher.delete_function(
            function_type=IGetUserEmailByPhoneQuery,
        )
        self.__dispatcher.delete_function(
            function_type=IGetUsersEmailAddresses,
        )
