from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping
from typing import Optional

from asterisk_amocrm.infrastructure import IGetCurrentAppVersionFunction
from asterisk_amocrm.infrastructure import ILogger
from asterisk_amocrm.infrastructure import ISelectableFactory

from .RabbitmqMessageBus import RabbitmqMessageBus
from .RabbitmqMessageBusConfig import RabbitmqMessageBusConfig
from ....core import InitializableMessageBus


__all__ = [
    "RabbitmqMessageBusFactory",
]


class RabbitmqMessageBusFactory(ISelectableFactory[InitializableMessageBus]):

    __slots__ = (
        "__get_app_version_function",
        "__event_loop",
        "__logger",
    )

    def __init__(
        self,
        get_app_version_function: IGetCurrentAppVersionFunction,
        event_loop: AbstractEventLoop,
        logger: ILogger,
    ) -> None:
        self.__get_app_version_function = get_app_version_function
        self.__event_loop = event_loop
        self.__logger = logger

    def unique_tag(self) -> str:
        return "rabbitmq"

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> InitializableMessageBus:
        settings = settings or {}

        config = RabbitmqMessageBusConfig(**settings)

        message_bus = RabbitmqMessageBus(
            config=config,
            get_app_version_function=self.__get_app_version_function,
            event_loop=self.__event_loop,
            logger=self.__logger,
        )

        return message_bus
