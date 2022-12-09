from typing import Any
from typing import Mapping
from typing import Optional

from amocrm_api_client import AmoCrmApiClient
from fastapi import FastAPI

from asterisk_ng.interfaces import IGetCrmUserIdByPhoneQuery
from asterisk_ng.interfaces import IOriginationDomainCommand
from asterisk_ng.system.dispatcher import IDispatcher

from asterisk_ng.system.container import container
from asterisk_ng.system.container import Key

from asterisk_ng.system.plugin import AbstractPlugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface

from .AsteriskPluginConfig import AsteriskPluginConfig
from .WidgetView import WidgetView


__all__ = ["AsteriskWidgetPlugin"]


class AsteriskWidgetPlugin(AbstractPlugin):

    __slots__ = (
        "__app",
        "__route",
    )

    def __init__(self) -> None:
        self.__app: Optional[FastAPI] = None
        self.__route = None

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            imported=Interface(
                container=[
                    Key(FastAPI),
                    Key(AmoCrmApiClient),
                ],
                dispatcher=[
                    IOriginationDomainCommand,
                    IGetCrmUserIdByPhoneQuery,
                ],
            )
        )

    async def upload(self, settings: Mapping[str, Any]) -> None:

        self.__app = container.resolve(Key(FastAPI))
        dispatcher = container.resolve(Key(IDispatcher))

        config = AsteriskPluginConfig(**settings)

        widget_view = WidgetView(
            config=config,
            origination_command=dispatcher.get_function(IOriginationDomainCommand),
            get_crm_user_id_by_phone_query=dispatcher.get_function(IGetCrmUserIdByPhoneQuery),
        )

        self.__app.add_api_route(
            path="/asterisk",
            endpoint=widget_view.handle,
            tags=["Widgets"],
            methods=["GET"]
        )

    async def unload(self) -> None:
        pass
