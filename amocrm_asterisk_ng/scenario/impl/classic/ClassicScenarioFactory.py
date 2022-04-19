from typing import Any
from typing import Mapping
from typing import Optional

from amocrm_asterisk_ng.infrastructure import IFactory
from amocrm_asterisk_ng.infrastructure import IEventBus
from amocrm_asterisk_ng.infrastructure import IDispatcher

from ...core import IScenario

from .ClassicScenario import ClassicScenario
from .ClassicScenarioConfig import ClassicScenarioConfig


__all__ = [
    "ClassicScenarioFactory",
]


class ClassicScenarioFactory(IFactory[IScenario]):

    __slots__ = (
        "__event_bus",
        "__dispatcher",
    )

    def __init__(
        self,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
    ) -> None:
        self.__event_bus = event_bus
        self.__dispatcher = dispatcher

    def get_instance(self, settings: Optional[Mapping[str, Any]] = None) -> IScenario:

        settings = settings or {}

        config = ClassicScenarioConfig(**settings)

        return ClassicScenario(
            config=config,
            event_bus=self.__event_bus,
            dispatcher=self.__dispatcher,
        )
