from fastapi import FastAPI
from asterisk_amocrm.infrastructure import (
    IDispatcher,
    IComponent,
    ILogger,
)
from .AsteriskWidgetConfig import AsteriskWidgetConfig
from .views import OriginationView
from .query_handlers import (
    IGetUserEmailByPhoneQH,
    GetUserEmailByPhoneQH,
)


__all__ = [
    "AsteriskWidgetComponent",
]


class AsteriskWidgetComponent(IComponent):

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

        await self.__dispatcher.attach_query_handler(
            IGetUserEmailByPhoneQH,
            GetUserEmailByPhoneQH(
                users=self.__config.users,
                logger=self.__logger,
            )
        )

    async def deinitialize(self) -> None:

        await self.__dispatcher.detach_query_handler(
            GetUserEmailByPhoneQH,
        )
