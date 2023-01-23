from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping

from panoramisk import Manager

from asterisk_ng.system.logger import ILogger

from .AmiManagerComponent import AmiManagerComponent
from .AmiManagerConfig import AmiManagerConfig

from ..core import IAmiManagerComponent


__all__ = ["AmiManagerComponentFactory"]


class AmiManagerComponentFactory:

    __slots__ = (
        "__event_loop",
        "__logger",
    )

    def __init__(
        self,
        event_loop: AbstractEventLoop,
        logger: ILogger,
    ) -> None:
        self.__event_loop = event_loop
        self.__logger = logger

    def __call__(self, settings: Mapping[str, Any]) -> IAmiManagerComponent:

        config = AmiManagerConfig(**settings)

        panoramisk_manager = Manager(
            host=config.host,
            port=config.port,
            username=config.user,
            secret=config.secret,
            loop=self.__event_loop,
        )

        ami_manager = AmiManagerComponent(
            manager=panoramisk_manager,
            logger=self.__logger,
        )

        return ami_manager
