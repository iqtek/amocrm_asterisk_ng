from abc import ABC
from enum import IntEnum

from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Optional
from typing import Union


__all__ = [
    "Level",
    "Message",
    "ILogger",
    "ILoggerFactory",
    "InitializableLogger",
]


class Level(IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


Message = Union[str, Callable[[], str], Coroutine[Any, Any, str]]


class ILogger(ABC):

    __slots__ = ()

    async def log(self, level: Level, message: Message, exception: Optional[Exception] = None) -> None:
        raise NotImplementedError()

    async def debug(self, message: Message) -> None:
        raise NotImplementedError()

    async def info(self, message: Message) -> None:
        raise NotImplementedError()

    async def warning(self, message: Message, exception: Optional[Exception] = None) -> None:
        raise NotImplementedError()

    async def error(self, message: Message, exception: Optional[Exception] = None) -> None:
        raise NotImplementedError()

    async def critical(self, message: Message, exception: Optional[Exception] = None) -> None:
        raise NotImplementedError()
