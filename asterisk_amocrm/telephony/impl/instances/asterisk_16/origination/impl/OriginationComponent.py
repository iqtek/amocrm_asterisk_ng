from asterisk_amocrm.infrastructure import IComponent, IDispatcher, IEventBus
from .OriginationCallCH import OriginationCallCH
from .OriginationConfig import OriginationConfig
from .OriginationRequestEventHandler import OriginationRequestEventHandler
from ..core import IOriginationCallCH
from ......core import IAmiManager


__all__ = [
    "OriginationComponent",
]


class OriginationComponent(IComponent):

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

        await self.__dispatcher.attach_command_handler(
            IOriginationCallCH,
            OriginationCallCH(
                config=self.__config,
                ami_manager=self.__ami_manager,
            ),
        )

        await self.__event_bus.attach_event_handler(
            OriginationRequestEventHandler(
                dispatcher=self.__dispatcher,
            )
        )

    async def deinitialize(self) -> None:

        await self.__dispatcher.detach_command_handler(
            OriginationCallCH
        )

        await self.__event_bus.detach_event_handler(
            OriginationRequestEventHandler
        )
