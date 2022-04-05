from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping
from typing import Optional

from asterisk_amocrm.infrastructure import ILogger, IMessageBus, ISelectableFactory
from asterisk_amocrm.infrastructure import IMakeContextSnapshotFunction
from asterisk_amocrm.infrastructure import ISetContextVarsFunction

from .consumer import ConsumerFactory
from .event_serialization import EventToBytesSerializer
from .event_serialization import RegisteringFactory
from .ExtendedEventBus import ExtendedEventBus
from .ExtendedEventBusConfig import ExtendedEventBusConfig
from .....core import IEventBus


__all__ = [
    "ExtendedEventBusFactory",
]


class ExtendedEventBusFactory(ISelectableFactory[IEventBus]):

    def __init__(
        self,
        message_bus: IMessageBus,
        event_loop: AbstractEventLoop,
        set_context_vars_function: ISetContextVarsFunction,
        make_context_vars_snapshot: IMakeContextSnapshotFunction,
        logger: ILogger,
    ) -> None:
        self.__message_bus = message_bus
        self.__event_loop = event_loop
        self.__set_context_vars_function = set_context_vars_function
        self.__make_context_vars_snapshot = make_context_vars_snapshot
        self.__logger = logger

    def unique_tag(self) -> str:
        return "extended"

    def get_instance(self, settings: Optional[Mapping[str, Any]] = None) -> IEventBus:
        settings = {}

        config = ExtendedEventBusConfig(**settings)

        event_factory = RegisteringFactory()

        event_to_bytes_serializer = EventToBytesSerializer(
            event_factory=event_factory,
        )

        consumer_factory = ConsumerFactory(
            event_to_bytes_serializer=event_to_bytes_serializer,
            set_context_vars_function=self.__set_context_vars_function,
            message_bus=self.__message_bus,
            logger=self.__logger,
        )

        return ExtendedEventBus(
            config=config,
            message_bus=self.__message_bus,
            event_factory=event_factory,
            consumer_factory=consumer_factory,
            event_to_bytes_serializer=event_to_bytes_serializer,
            make_context_vars_snapshot=self.__make_context_vars_snapshot,
            logger=self.__logger,
        )

