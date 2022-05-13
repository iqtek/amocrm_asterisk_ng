from typing import Any
from typing import Mapping
from typing import Optional

from glassio.dispatcher import IDispatcher
from glassio.mixins import IFactory
from glassio.initializable_components import InitializableComponent

from .OriginationComponent import OriginationComponent
from .OriginationConfig import OriginationConfig
from .....core import IAmiManager


__all__ = [
    "OriginationComponentFactory",
]


class OriginationComponentFactory(IFactory[InitializableComponent]):

    __slots__ = (
        "__ami_manager",
        "__dispatcher",
    )

    def __init__(
        self,
        ami_manager: IAmiManager,
        dispatcher: IDispatcher,
    ) -> None:
        self.__ami_manager = ami_manager
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
            dispatcher=self.__dispatcher,
        )

        return origination_component
