from asyncio import AbstractEventLoop

from typing import Optional
from typing import TypeVar

from asterisk_amocrm.infrastructure import ILogger

from ...AbstractEventBus import AbstractEventBus
from ....core import IEvent
from ....core import IEventHandler
from ....core import InitializableEventBus


__all__ = [
    "MemoryEventBus",
]


T = TypeVar('T', bound=IEvent)
H = TypeVar('H', bound=IEventHandler)


class MemoryEventBus(AbstractEventBus, InitializableEventBus):

    __slots__ = (
        "__event_loop",
        "__logger",
    )

    def __init__(
        self,
        logger: ILogger,
        event_loop: AbstractEventLoop
    ) -> None:
        super().__init__(logger=logger)
        self.__event_loop = event_loop
        self.__logger = logger

    async def initialize(self) -> None:
        pass

    async def deinitialize(self) -> None:
        pass

    async def publish(self, event: IEvent) -> None:
        self.__logger.debug(
            "EventBus: "
            f"event captured: {event}."
        )
        self.__event_loop.create_task(self._publish(event))
