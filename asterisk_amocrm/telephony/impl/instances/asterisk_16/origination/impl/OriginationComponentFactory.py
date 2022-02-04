from typing import Any, Mapping

from asterisk_amocrm.infrastructure import IComponent, IDispatcher, IEventBus
from .OriginationComponent import OriginationComponent
from .OriginationConfig import OriginationConfig
from ......core import IAmiManager


__all__ = [
    "OriginationComponentFactory",
]


class OriginationComponentFactory:

    def __init__(
        self,
        ami_manager: IAmiManager,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
    ) -> None:
        self.__ami_manager = ami_manager
        self.__event_bus = event_bus
        self.__dispatcher = dispatcher

    def get_instance(self, settings: Mapping[str, Any]) -> IComponent:

        config = OriginationConfig(**settings)

        origination_component = OriginationComponent(
            config=config,
            ami_manager=self.__ami_manager,
            event_bus=self.__event_bus,
            dispatcher=self.__dispatcher,
        )

        return origination_component
