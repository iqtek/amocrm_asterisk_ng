from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping
from typing import Optional

from panoramisk import Manager

from amocrm_asterisk_ng.infrastructure import IFactory
from amocrm_asterisk_ng.infrastructure import ILogger

from .AmiManagerConfig import AmiManagerConfig
from .AmiManagerImpl import AmiManagerImpl
from ...core import IAmiManager
from ...core import IAmiMessageConvertFunction


__all__ = [
    "AmiManagerFactory",
]


class AmiManagerFactory(IFactory[IAmiManager]):

    __slots__ = (
        "__event_loop",
        "__ami_message_convert_function",
        "__logger",
    )

    def __init__(
        self,
        event_loop: AbstractEventLoop,
        ami_message_convert_function: IAmiMessageConvertFunction,
        logger: ILogger,
    ) -> None:
        self.__event_loop = event_loop
        self.__ami_message_convert_function = ami_message_convert_function
        self.__logger = logger

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> IAmiManager:
        settings = settings or {}

        config = AmiManagerConfig(**settings)

        panoramisk_manager = Manager(
            host=config.host,
            port=config.port,
            username=config.user,
            secret=config.secret,
            loop=self.__event_loop,
        )

        ami_manager = AmiManagerImpl(
            manager=panoramisk_manager,
            ami_message_convert_function=self.__ami_message_convert_function,
            logger=self.__logger,
        )

        return ami_manager
