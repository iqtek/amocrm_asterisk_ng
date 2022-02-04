from typing import TypeVar
from .ICommand import ICommand


__all__ = [
    "ICommandHandler",
]


C = TypeVar('C', bound=ICommand)


class ICommandHandler:

    async def __call__(self, command: C) -> None:
        raise NotImplementedError()

    def __str__(self) -> str:
        return "{}".format(self.__class__.__name__)
