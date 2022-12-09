from typing import Any
from typing import Mapping

from fastapi import FastAPI

from asterisk_ng.interfaces import IGetResponsibleUserByPhoneQuery

from asterisk_ng.system.container import container
from asterisk_ng.system.container import Key
from asterisk_ng.system.dispatcher import IDispatcher

from asterisk_ng.system.plugin import AbstractPlugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface

from .RedirectingView import RedirectingView


__all__ = ["RedirectingPlugin"]


class RedirectingPlugin(AbstractPlugin):

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            imported=Interface(
                dispatcher=[IGetResponsibleUserByPhoneQuery],
                container=[Key(FastAPI)]
            )
        )

    async def upload(self, settings: Mapping[str, Any]) -> None:
        dispatcher = container.resolve(Key(IDispatcher))
        app = container.resolve(Key(FastAPI))

        redirecting_view = RedirectingView(
            get_responsible_user_by_phone_query=dispatcher.get_function(IGetResponsibleUserByPhoneQuery)
        )

        app.add_api_route(
            path="/redirecting",
            endpoint=redirecting_view.handle,
            methods=["GET"],
            tags=["Redirecting"]
        )

    async def unload(self) -> None:
        pass
