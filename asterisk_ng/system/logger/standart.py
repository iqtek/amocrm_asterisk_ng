from asyncio import AbstractEventLoop
from asyncio import get_running_loop
from asyncio import iscoroutine

from contextvars import copy_context

import logging
from typing import Optional

from .abstract import AbstractLogger
from .core import Level
from .core import Message


__all__ = [
    "StandardLogger",
]


class StandardLogger(AbstractLogger):

    __slots__ = (
        "__event_loop",
        "__logger",
    )

    __LOGGING_LEVELS = {
        Level.DEBUG: logging.DEBUG,
        Level.INFO: logging.INFO,
        Level.WARNING: logging.WARNING,
        Level.ERROR: logging.ERROR,
        Level.CRITICAL: logging.CRITICAL,
    }

    def __init__(
        self,
        logger: logging.Logger,
        event_loop: Optional[AbstractEventLoop] = None
    ) -> None:
        super().__init__()
        self.__event_loop = event_loop
        self.__logger = logger

    async def log(self, level: Level, message: Message, exception: Optional[Exception] = None) -> None:

        if self.__event_loop is None:
            self.__event_loop = get_running_loop()

        if not self.__is_enabled(level):
            return

        if isinstance(message, str):
            pass

        elif iscoroutine(message):
            message = await message

        elif callable(message):
            message = message()

        else:
            return
        current_context = copy_context()

        def log() -> None:
            current_context.run(self.__logger.log, self.__convert_level(level), message, exc_info=exception)

        return await self.__event_loop.run_in_executor(None, log)

    def __is_enabled(self, level: Level) -> bool:
        return self.__logger.isEnabledFor(self.__convert_level(level))

    def __convert_level(self, level: Level) -> int:
        return self.__LOGGING_LEVELS[level]
