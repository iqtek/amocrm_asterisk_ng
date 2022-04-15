from typing import Any
from typing import Mapping
from typing import Optional

from amocrm_asterisk_ng.infrastructure import InitializableComponent
from amocrm_asterisk_ng.infrastructure import IFactory
from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import IEventBus

from .OriginationComponent import OriginationComponent
from .OriginationConfig import OriginationConfig
from ......core import IAmiManager


__all__ = [
    "OriginationComponentFactory",
]


class OriginationComponentFactory(IFactory[InitializableComponent]):

    __slots__ = (
        "__ami_manager",
        "__event_bus",
        "__dispatcher",
    )

    def __init__(
        self,
        ami_manager: IAmiManager,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
    ) -> None:
        self.__ami_manager = ami_manager
        self.__event_bus = event_bus
        self.__dispatcher = dispatcher

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> InitializableComponent:

        settings = settings or {}

        config = OriginationConfig(**settings)

        origination_component = OriginationComponent(
            config=config,
            ami_manager=self.__ami_manager,
            event_bus=self.__event_bus,
            dispatcher=self.__dispatcher,
        )

        return origination_component
