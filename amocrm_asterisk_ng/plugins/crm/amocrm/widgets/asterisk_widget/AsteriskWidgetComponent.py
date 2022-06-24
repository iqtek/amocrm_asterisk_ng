from typing import Optional

from fastapi import FastAPI
from glassio.dispatcher import IDispatcher
from glassio.initializable_components import AbstractInitializableComponent

from amocrm_asterisk_ng.domain import IsOperatorPhoneNumerQuery

from ...core import IGetOperatorsEmailAddressesQuery

from .functions import GetOperatorsEmailAddressesQuery
from .functions import IsOperatorPhoneNumerQueryImpl
from .WidgetView import WidgetView
from .AsteriskWidgetConfig import AsteriskWidgetConfig


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
            function_type=IGetOperatorsEmailAddressesQuery,
            function=GetOperatorsEmailAddressesQuery(
                users=self.__config.users,
            )
        )
        self.__dispatcher.add_function(
            function_type=IsOperatorPhoneNumerQuery,
            function=IsOperatorPhoneNumerQueryImpl(
                users=self.__config.users,
            )
        )

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        self.__dispatcher.delete_function(IsOperatorPhoneNumerQuery)
        self.__dispatcher.delete_function(IGetOperatorsEmailAddressesQuery)
