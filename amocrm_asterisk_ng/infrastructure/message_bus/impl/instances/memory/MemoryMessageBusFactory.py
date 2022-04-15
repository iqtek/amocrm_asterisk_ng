from asyncio import AbstractEventLoop
from asyncio import PriorityQueue
from typing import Any
from typing import Mapping
from typing import Optional

from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import ISelectableFactory

from .MemoryMessageBus import MemoryMessageBus
from ....core import InitializableMessageBus


__all__ = [
    "MemoryMessageBusFactory",
]


class MemoryMessageBusFactory(ISelectableFactory[InitializableMessageBus]):

    __slots__ = (
        "__event_loop",
        "__logger",
    )

    def __init__(
        self,
        event_loop: AbstractEventLoop,
        logger: ILogger,
    ) -> None:
        self.__event_loop = event_loop
        self.__logger = logger

    def unique_tag(self) -> str:
        return "memory"

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> InitializableMessageBus:

        queue = PriorityQueue()

        return MemoryMessageBus(
            queue=queue,
            event_loop=self.__event_loop,
            logger=self.__logger,
        )
