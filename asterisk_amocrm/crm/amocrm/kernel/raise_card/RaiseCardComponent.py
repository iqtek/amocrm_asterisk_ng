from amo_crm_api_client import AmoCrmApiClient
from asterisk_amocrm.infrastructure import (
    IComponent,
    IEventBus,
    IDispatcher,
    ILogger,
)
from .command_handlers import (
    IRaiseCardCH,
    RaiseCardCH,
)
from .event_handlers import RingingEventHandler


__all__ = [
    "RaiseCardComponent",
]


class RaiseCardComponent(IComponent):

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        self.__amo_client = amo_client
        self.__event_bus = event_bus
        self.__dispatcher = dispatcher
        self.__logger = logger

    async def initialize(self) -> None:

        await self.__dispatcher.attach_command_handler(
            IRaiseCardCH,
            RaiseCardCH(
                amo_client=self.__amo_client,
                logger=self.__logger,
            )
        )

        await self.__event_bus.attach_event_handler(
            RingingEventHandler(
                dispatcher=self.__dispatcher,
                logger=self.__logger,
            )
        )

    async def deinitialize(self) -> None:

        await self.__event_bus.detach_event_handler(
            RingingEventHandler,
        )

        await self.__dispatcher.detach_command_handler(
            RaiseCardCH,
        )
