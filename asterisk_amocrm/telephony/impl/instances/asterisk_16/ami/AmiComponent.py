import asyncio

from asterisk_amocrm.infrastructure import (
    IComponent,
    IEventBus,
    ILogger,
)
from .ami_handlers import (
    CdrEventHandler,
    DialBeginEventHandler,
    HangupEventHandler,
    NewCallerIdEventHandler,
    NewChannelEventHandler,
    NewStateEventHandler,
)
from .ami_store import IAmiStore
from .....core import IAmiManager


__all__ = [
    "AmiComponent"
]


class AmiComponent(IComponent):

    def __init__(
        self,
        ami_manager: IAmiManager,
        ami_store: IAmiStore,
        event_bus: IEventBus,
        logger: ILogger,
    ) -> None:
        self.__ami_manager = ami_manager
        self.__ami_store = ami_store
        self.__event_bus = event_bus
        self.__logger = logger

    async def initialize(self) -> None:
        self.__ami_manager.connect()
        await asyncio.sleep(1)

        self.__ami_manager.attach_event_handler(
            NewChannelEventHandler(
                ami_store=self.__ami_store,
                logger=self.__logger,
            )
        )
        self.__ami_manager.attach_event_handler(
            HangupEventHandler(
                ami_store=self.__ami_store,
                logger=self.__logger,
            )
        )
        self.__ami_manager.attach_event_handler(
            DialBeginEventHandler(
                ami_store=self.__ami_store,
                logger=self.__logger,
            )
        )
        self.__ami_manager.attach_event_handler(
            NewCallerIdEventHandler(
                ami_store=self.__ami_store,
                logger=self.__logger,
            )
        )
        self.__ami_manager.attach_event_handler(
            NewStateEventHandler(
                event_bus=self.__event_bus,
                ami_store=self.__ami_store,
                logger=self.__logger,
            )
        )
        self.__ami_manager.attach_event_handler(
            CdrEventHandler(
                event_bus=self.__event_bus,
                ami_store=self.__ami_store,
                logger=self.__logger,
            )
        )

    async def deinitialize(self) -> None:
        self.__ami_manager.disconnect()
