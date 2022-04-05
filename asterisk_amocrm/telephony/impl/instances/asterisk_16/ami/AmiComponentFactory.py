from asyncio import AbstractEventLoop

from asterisk_amocrm.infrastructure import InitializableComponent
from asterisk_amocrm.infrastructure import IEventBus
from asterisk_amocrm.infrastructure import IKeyValueStorage
from asterisk_amocrm.infrastructure import ILogger

from .ami_store import AmiStoreImpl
from .AmiComponent import AmiComponent
from .....core import IAmiManager


__all__ = [
    "AmiComponentFactory",
]


class AmiComponentFactory:

    def __init__(
        self,
        ami_manager: IAmiManager,
        storage: IKeyValueStorage,
        event_bus: IEventBus,
        event_loop: AbstractEventLoop,
        logger: ILogger,
    ) -> None:
        self.__ami_manager = ami_manager
        self.__storage = storage
        self.__event_bus = event_bus
        self.__event_loop = event_loop
        self.__logger = logger

    def get_instance(self) -> InitializableComponent:

        ami_store = AmiStoreImpl(
            storage=self.__storage,
            logger=self.__logger,
        )

        return AmiComponent(
            ami_manager=self.__ami_manager,
            ami_store=ami_store,
            event_bus=self.__event_bus,
            logger=self.__logger,
        )
