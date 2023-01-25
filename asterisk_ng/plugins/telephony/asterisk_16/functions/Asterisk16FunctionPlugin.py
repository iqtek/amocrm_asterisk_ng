from typing import Any
from typing import Mapping
from typing import Optional

from asterisk_ng.interfaces import IHangupTelephonyCommand
from asterisk_ng.interfaces import IOriginationTelephonyCommand
from asterisk_ng.interfaces import IRedirectTelephonyCommand
from asterisk_ng.interfaces import ISetMuteTelephonyCommand

from asterisk_ng.plugins.telephony.ami_manager import IAmiManager
from asterisk_ng.plugins.telephony.asterisk_16.reflector import IReflector

from asterisk_ng.system.container import container
from asterisk_ng.system.container import Key
from asterisk_ng.system.dispatcher import IDispatcher
from asterisk_ng.system.event_bus import IEventBus
from asterisk_ng.system.plugin import AbstractPlugin, Interface, PluginInterface

from .Asterisk16FunctionPluginConfig import Asterisk16FunctionPluginConfig

from .impl import (
    HangupTelephonyCommandImpl,
    OriginationTelephonyCommandImpl,
    RedirectTelephonyCommandImpl,
    SetMuteTelephonyCommandImpl,
)


__all__ = ["Asterisk16FunctionPlugin"]


class Asterisk16FunctionPlugin(AbstractPlugin):

    __slots__ = (
        "__dispatcher",
    )

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            imported=Interface(
                container=[
                    Key(IAmiManager),
                    Key(IReflector),
                ],
            ),
            exported=Interface(
                dispatcher=[
                    IOriginationTelephonyCommand,
                    IHangupTelephonyCommand,
                    IRedirectTelephonyCommand,
                    ISetMuteTelephonyCommand
                ],
            )
        )

    def __init__(self) -> None:
        self.__dispatcher: Optional[IDispatcher] = None

    async def upload(self, settings: Mapping[str, Any]) -> None:

        self.__dispatcher = container.resolve(Key(IDispatcher))

        event_bus = container.resolve(Key(IEventBus))
        ami_manager = container.resolve(Key(IAmiManager))
        reflector = container.resolve(Key(IReflector))

        config = Asterisk16FunctionPluginConfig(**settings)

        self.__dispatcher.add_function(
            IOriginationTelephonyCommand,
            OriginationTelephonyCommandImpl(
                ami_manager=ami_manager,
                context=config.origination_context,
                timeout=config.origination_timeout,
            )
        )

        self.__dispatcher.add_function(
            IHangupTelephonyCommand,
            HangupTelephonyCommandImpl(
                ami_manager=ami_manager,
                reflector=reflector,
            )
        )

        self.__dispatcher.add_function(
            IRedirectTelephonyCommand,
            RedirectTelephonyCommandImpl(
                ami_manager=ami_manager,
                reflector=reflector,
                event_bus=event_bus,
                context=config.redirect_context,
            )
        )

        self.__dispatcher.add_function(
            ISetMuteTelephonyCommand,
            SetMuteTelephonyCommandImpl(
                ami_manager=ami_manager,
                reflector=reflector,
                event_bus=event_bus,
            )
        )

    async def unload(self) -> None:
        self.__dispatcher.delete_function(IOriginationTelephonyCommand)
        self.__dispatcher.delete_function(IHangupTelephonyCommand)
        self.__dispatcher.delete_function(IRedirectTelephonyCommand)
        self.__dispatcher.delete_function(ISetMuteTelephonyCommand)
