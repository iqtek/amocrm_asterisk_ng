from typing import Type
from ..IEventHandler import IEventHandler


__all__ = [
    "HandlerNotAttachedFoundException",
    "HandlerAlreadyAttachedException",
]


class HandlerNotAttachedFoundException(Exception):

    def __init__(self, handler: Type[IEventHandler]) -> None:
        self.__handler = handler

    def __str__(self) -> str:
        return f"Handler with type={type(self.__handler)}" \
               f"not attached."


class HandlerAlreadyAttachedException(Exception):

    def __init__(self, handler: Type[IEventHandler]) -> None:
        self.__handler = handler

    def __str__(self) -> str:
        return f"Handler with type={type(self.__handler)}" \
               f"is already attached."

