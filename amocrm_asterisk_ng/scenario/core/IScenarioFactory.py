from typing import Any
from typing import Mapping

from glassio.dispatcher import IDispatcher
from glassio.event_bus import IEventBus
from glassio.logger import ILogger

from ..core import IScenario


__all__ = [
    "IScenarioFactory",
]


class IScenarioFactory:

    __slots__ = (
        "__event_bus",
        "__dispatcher",
        "__logger",
    )

    def initialize(
        self,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        raise NotImplementedError()

    def get_instance(self, settings: Mapping[str, Any]) -> IScenario:
        raise NotImplementedError()
