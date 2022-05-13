from typing import Optional

from fastapi import FastAPI
from glassio.dispatcher import IDispatcher
from glassio.initializable_components import AbstractInitializableComponent

from amocrm_asterisk_ng.domain import IsUserPhoneNumerQuery
from .AsteriskWidgetConfig import AsteriskWidgetConfig
from .GetUsersEmailAddressesQuery import GetUsersEmailAddressesQuery
from .IsUserPhoneNumerQueryImpl import IsUserPhoneNumerQueryImpl
from .WidgetView import WidgetView
from ...core import IGetUsersEmailAddressesQuery


__all__ = [
    "AsteriskWidgetComponent",
]


class AsteriskWidgetComponent(AbstractInitializableComponent):

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
        super().__init__()
        self.__config = config
        self.__app = app
        self.__dispatcher = dispatcher
        self.__widget_view = widget_view

    async def _initialize(self) -> None:

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
        self.__dispatcher.add_function(
            function_type=IsUserPhoneNumerQuery,
            function=IsUserPhoneNumerQueryImpl(
                users=self.__config.users,
            )
        )

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        self.__dispatcher.delete_function(
            function_type=IsUserPhoneNumerQuery,
        )
        self.__dispatcher.delete_function(
            function_type=IGetUsersEmailAddressesQuery,
        )
