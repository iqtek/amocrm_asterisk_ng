from fastapi import FastAPI

from asterisk_amocrm.infrastructure import IDispatcher
from asterisk_amocrm.infrastructure import ILogger
from asterisk_amocrm.infrastructure import InitializableComponent

from .AsteriskWidgetConfig import AsteriskWidgetConfig
from .query_handlers import GetUserEmailByPhoneQuery
from .views import OriginationView
from ...core import IGetUserEmailByPhoneQuery


__all__ = [
    "AsteriskWidgetComponent",
]


class AsteriskWidgetComponent(InitializableComponent):

    __slots__ = (
        "__config",
        "__app",
        "__dispatcher",
        "__origination_view",
        "__logger",
    )

    def __init__(
        self,
        config: AsteriskWidgetConfig,
        app: FastAPI,
        dispatcher: IDispatcher,
        origination_view: OriginationView,
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__app = app
        self.__dispatcher = dispatcher
        self.__origination_view = origination_view
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

    async def deinitialize(self) -> None:

        self.__dispatcher.delete_function(
            function_type=IGetUserEmailByPhoneQuery,
        )
