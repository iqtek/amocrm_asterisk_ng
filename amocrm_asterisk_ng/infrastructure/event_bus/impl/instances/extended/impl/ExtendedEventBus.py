from typing import Type

from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import IMessageBus
from amocrm_asterisk_ng.infrastructure import Properties
from .consumer import ConsumerFactory
from .ExtendedEventBusConfig import ExtendedEventBusConfig
from ..core import IRegisteringFactory
from ..core import ISerializer
from ....AbstractEventBus import AbstractEventBus
from .....core import IEvent
from .....core import IEventHandler
from .....core import InitializableEventBus


__all__ = [
    "ExtendedEventBus",
]


class ExtendedEventBus(AbstractEventBus, InitializableEventBus):

    __slots__ = (
        "__config",
        "__event_to_bytes_serializer",
        "__event_factory",
        "__message_bus",
        "__consumer_factory",
        "__logger",
    )

    def __init__(
        self,
        config: ExtendedEventBusConfig,
        message_bus: IMessageBus,
        consumer_factory: ConsumerFactory,
        event_factory: IRegisteringFactory[IEvent],
        event_to_bytes_serializer: ISerializer[IEvent, bytes],
        logger: ILogger,
    ) -> None:
        super().__init__(logger=logger)
        self.__config = config
        self.__message_bus = message_bus
        self.__consumer_factory = consumer_factory
        self.__event_factory = event_factory
        self.__event_to_bytes_serializer = event_to_bytes_serializer
        self.__logger = logger

    async def attach_event_handler(self, event_handler: IEventHandler) -> None:
        event_type = super()._get_event_type(event_handler)
        event_name = event_type.__name__
        self.__event_factory.register_type(
            type_name=event_name,
            obj_type=event_type,
        )
        await super().attach_event_handler(event_handler=event_handler)

    async def detach_event_handler(self, event_handler: Type[IEventHandler]) -> None:
        event_type = self._get_event_type(event_handler)
        event_name = event_type.__name__
        await super().detach_event_handler(event_handler=event_handler)
        self.__event_factory.unregister_type(
            type_name=event_name,
        )

    async def publish(self, event: IEvent) -> None:
        try:
            message = self.__event_to_bytes_serializer.serialize(event)
        except Exception as e:
            self.__logger.error(
                "ExtendedEventBus: "
                "Unable to serialize event to message: "
                f"`{event}`. {e}."
            )
            raise e
        await self.__message_bus.publish(
            message=message,
            properties=Properties()
        )

    async def initialize(self) -> None:
        for _ in range(self.__config.workers):
            await self.__message_bus.add_consumer(
                self.__consumer_factory.get_instance(super()._publish)
            )

    async def deinitialize(self) -> None:
        pass
