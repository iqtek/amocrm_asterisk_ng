from typing import Type

from ..IEventHandler import IEventHandler


__all__ = [
    "HandlerAlreadyAttachedException",
]


class HandlerAlreadyAttachedException(Exception):

    def __init__(self, handler_type: Type[IEventHandler]) -> None:
        self.__handler_type = handler_type

    def __str__(self) -> str:
        return f"Handler with type: '{self.__handler_type}' " \
               f"is already attached."
