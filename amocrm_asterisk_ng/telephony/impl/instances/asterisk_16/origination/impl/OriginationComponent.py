from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import IEventBus
from amocrm_asterisk_ng.infrastructure import InitializableComponent

from .OriginationCallCommand import OriginationCallCommand
from .OriginationConfig import OriginationConfig
from .OriginationRequestEventHandler import OriginationRequestEventHandler
from ..core import IOriginationCallCommand
from ......core import IAmiManager


__all__ = [
    "OriginationComponent",
]


class OriginationComponent(InitializableComponent):

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
        event_bus: IEventBus,
        dispatcher: IDispatcher,
    ) -> None:
        self.__config = config
        self.__ami_manager = ami_manager
        self.__event_bus = event_bus
        self.__dispatcher = dispatcher

    async def initialize(self) -> None:

        self.__dispatcher.add_function(
            function_type=IOriginationCallCommand,
            function=OriginationCallCommand(
                config=self.__config,
                ami_manager=self.__ami_manager,
            ),
        )

        origination_call_command = self.__dispatcher.get_function(IOriginationCallCommand)

        await self.__event_bus.attach_event_handler(
            OriginationRequestEventHandler(
                origination_call_command=origination_call_command,
            )
        )

    async def deinitialize(self) -> None:

        self.__dispatcher.delete_function(
            function_type=IOriginationCallCommand,
        )

        await self.__event_bus.detach_event_handler(
            OriginationRequestEventHandler
        )
