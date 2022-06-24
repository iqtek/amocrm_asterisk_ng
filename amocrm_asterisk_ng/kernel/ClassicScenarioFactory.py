from typing import Any
from typing import Mapping
from typing import Optional

from glassio.dispatcher import IDispatcher
from glassio.event_bus import IEventBus
from glassio.logger import ILogger

from .ClassicScenario import ClassicScenario
from .ClassicScenarioConfig import ClassicScenarioConfig
from ....core import IScenario
from ....core import IScenarioFactory


__all__ = [
    "ClassicScenarioFactory",
]


class ClassicScenarioFactory(IScenarioFactory):

    __slots__ = (
        "__event_bus",
        "__dispatcher",
        "__logger",
    )

    def __init__(self) -> None:
        self.__event_bus = None
        self.__dispatcher = None
        self.__logger = None

    def initialize(
        self,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        self.__event_bus = event_bus
        self.__dispatcher = dispatcher
        self.__logger = logger

    def get_instance(self, settings: Mapping[str, Any]) -> IScenario:

        config = ClassicScenarioConfig(**settings)

        return ClassicScenario(
            config=config,
            event_bus=self.__event_bus,
            dispatcher=self.__dispatcher,
            logger=self.__logger,
        )
