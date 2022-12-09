from typing import Any
from typing import Mapping

from asterisk_ng.system.container import container
from asterisk_ng.system.container import Key
from asterisk_ng.system.container import SingletonResolver

from asterisk_ng.system.logger import ILogger

from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import AbstractPlugin
from asterisk_ng.system.plugin import PluginInterface

from asterisk_ng.plugins.system.storage import IKeyValueStorage
from asterisk_ng.system.event_bus import IEventBus
from asterisk_ng.plugins.telephony.ami_manager import IAmiManager

from .core import IReflector
from .impl import ReflectorImpl

from .impl.handlers import NewChannelEventHandler
from .impl.handlers import HangupEventHandler
from .impl.handlers import NewStateEventHandler
from .impl.handlers import NewCallerIdEventHandler
from .impl.handlers import DialStateEventHandler
from .impl.handlers import CdrEventHandler
from .impl.handlers import BridgeCreateEventHandler
from .impl.handlers import BridgeDestroyEventHandler
from .impl.handlers import BridgeLeaveEventHandler
from .impl.handlers import BridgeEnterEventHandler


__all__ = ["ReflectorPlugin"]


class ReflectorPlugin(AbstractPlugin):

    __slots__ = ()

    def __init__(self) -> None:
        pass

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

    async def upload(self, settings: Mapping[str, Any]) -> None:

        logger = container.resolve(Key(ILogger))
        storage = container.resolve(Key(IKeyValueStorage))
        event_bus = container.resolve(Key(IEventBus))
        ami_manager = container.resolve(Key(IAmiManager))

        reflector = ReflectorImpl(
            storage=storage,
            logger=logger,
        )

        ami_manager.attach_event_handler("BridgeCreate", BridgeCreateEventHandler(reflector, event_bus, logger))
        ami_manager.attach_event_handler("BridgeDestroy", BridgeDestroyEventHandler(reflector, event_bus, logger))
        ami_manager.attach_event_handler("BridgeEnter", BridgeEnterEventHandler(reflector, event_bus, logger))
        ami_manager.attach_event_handler("BridgeLeave", BridgeLeaveEventHandler(reflector, event_bus, logger))

        ami_manager.attach_event_handler("Newchannel", NewChannelEventHandler(reflector, logger))
        ami_manager.attach_event_handler("Newstate", NewStateEventHandler(reflector, event_bus, logger))
        ami_manager.attach_event_handler("NewCallerid", NewCallerIdEventHandler(reflector, logger))
        ami_manager.attach_event_handler("DialState", DialStateEventHandler(reflector, event_bus, logger))
        ami_manager.attach_event_handler("Hangup", HangupEventHandler(reflector, logger))
        ami_manager.attach_event_handler("Cdr", CdrEventHandler(reflector, event_bus, logger))

        container.set_resolver(Key(IReflector), SingletonResolver(reflector))

    async def unload(self) -> None:
        container.delete_resolver(Key(IReflector))
