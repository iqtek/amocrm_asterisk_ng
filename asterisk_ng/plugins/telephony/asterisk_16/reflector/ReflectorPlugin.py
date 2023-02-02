from re import compile
from re import search
from typing import Any
from typing import Mapping

from asterisk_ng.plugins.system.storage import IKeyValueStorage
from asterisk_ng.plugins.telephony.ami_manager import IAmiManager

from asterisk_ng.system.container import container
from asterisk_ng.system.container import Key
from asterisk_ng.system.container import SingletonResolver
from asterisk_ng.system.event_bus import IEventBus
from asterisk_ng.system.logger import ILogger

from asterisk_ng.system.plugin import AbstractPlugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface

from .core import IReflector
from .impl import CdrEventHandler
from .impl import HangupEventHandler
from .impl import NewCallerIdEventHandler
from .impl import NewChannelEventHandler
from .impl import NewStateEventHandler
from .impl import ReflectorImpl

from .ReflectorPluginConfig import ReflectorPluginConfig


__all__ = ["ReflectorPlugin"]


class ReflectorPlugin(AbstractPlugin):

    __slots__ = (
        "__internal_channel_pattern",
    )

    def __init__(self) -> None:
        self.__internal_channel_pattern = None

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            imported=Interface(
                container=[
                    Key(ILogger),
                    Key(IKeyValueStorage),
                    Key(IAmiManager),
                    Key(IEventBus),
                ],
            ),
            exported=Interface(
                container=[Key(IReflector)],
            )
        )

    def __is_physical_channel(self, channel_name: str) -> bool:
        return channel_name.startswith("PJSIP") or channel_name.startswith("SIP")

    def __get_phone_by_channel_name(self, channel_name: str):
        result = search(self.__internal_channel_pattern, channel_name)
        if result is not None:
            try:
                return result.group(1)
            except IndexError:
                pass

    async def upload(self, settings: Mapping[str, Any]) -> None:

        config = ReflectorPluginConfig(**settings)

        logger = container.resolve(Key(ILogger))
        storage = container.resolve(Key(IKeyValueStorage))
        event_bus = container.resolve(Key(IEventBus))
        ami_manager = container.resolve(Key(IAmiManager))

        reflector = ReflectorImpl(
            storage=storage,
            logger=logger,
        )

        self.__internal_channel_pattern = compile(config.internal_number_pattern)

        ami_manager.attach_event_handler(
            "Newchannel",
            NewChannelEventHandler(
                is_physical_channel=self.__is_physical_channel,
                get_phone_by_channel_name=self.__get_phone_by_channel_name,
                reflector=reflector,
            )
        )
        ami_manager.attach_event_handler(
            "Newstate",
            NewStateEventHandler(
                is_physical_channel=self.__is_physical_channel,
                reflector=reflector,
                event_bus=event_bus,
                logger=logger
            )
        )
        ami_manager.attach_event_handler(
            "NewCallerid",
            NewCallerIdEventHandler(
                is_physical_channel=self.__is_physical_channel,
                reflector=reflector,
                logger=logger
            )
        )
        ami_manager.attach_event_handler(
            "Hangup",
            HangupEventHandler(
                is_physical_channel=self.__is_physical_channel,
                reflector=reflector,
                event_bus=event_bus,
                logger=logger
            )
        )
        ami_manager.attach_event_handler(
            "Cdr",
            CdrEventHandler(
                reflector=reflector,
                event_bus=event_bus,
                logger=logger
            )
        )

        container.set_resolver(Key(IReflector), SingletonResolver(reflector))

    async def unload(self) -> None:
        container.delete_resolver(Key(IReflector))
