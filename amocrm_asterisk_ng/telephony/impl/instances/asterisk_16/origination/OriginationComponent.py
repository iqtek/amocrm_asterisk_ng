from amocrm_asterisk_ng.domain import IOriginationCallCommand
from glassio.dispatcher import IDispatcher
from glassio.initializable_components import AbstractInitializableComponent
from typing import Optional
from .OriginationCallCommand import OriginationCallCommand
from .OriginationConfig import OriginationConfig
from .....core import IAmiManager


__all__ = [
    "OriginationComponent",
]


class OriginationComponent(AbstractInitializableComponent):

    __slots__ = (
        "__config",
        "__ami_manager",
        "__event_bus",
        "__dispatcher",
    )

    def __init__(
        self,
        config: OriginationConfig,
        ami_manager: IAmiManager,
        dispatcher: IDispatcher,
    ) -> None:
        super().__init__()
        self.__config = config
        self.__ami_manager = ami_manager
        self.__dispatcher = dispatcher

    async def _initialize(self) -> None:

        self.__dispatcher.add_function(
            function_type=IOriginationCallCommand,
            function=OriginationCallCommand(
                config=self.__config,
                ami_manager=self.__ami_manager,
            ),
        )

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:

        self.__dispatcher.delete_function(
            function_type=IOriginationCallCommand,
        )
