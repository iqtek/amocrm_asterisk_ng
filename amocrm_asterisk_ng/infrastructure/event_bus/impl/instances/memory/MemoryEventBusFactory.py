from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping
from typing import Optional

from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import ISelectableFactory

from .MemoryEventBus import MemoryEventBus
from ....core import IEventBus

__all__ = [
    "MemoryEventBusFactory",
]


class MemoryEventBusFactory(ISelectableFactory[IEventBus]):

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

    def get_instance(self, settings: Optional[Mapping[str, Any]] = None) -> IEventBus:
        return MemoryEventBus(
            event_loop=self.__event_loop,
            logger=self.__logger
        )
