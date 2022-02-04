from typing import (
    TypeVar,
    Type,
    Any,
)
from .IQuery import IQuery
from .ICommand import ICommand
from .IQueryHandler import IQueryHandler
from .ICommandHandler import ICommandHandler


__all__ = [
    "IDispatcher",
]


class IDispatcher:

    async def attach_query_handler(
        self,
        interface_type: Type,
        query_handler: IQueryHandler
    ) -> None:
        raise NotImplementedError()

    async def attach_command_handler(
        self,
        interface_type: Type,
        command_handler: ICommandHandler
    ) -> None:
        raise NotImplementedError()

    async def detach_query_handler(self, handler_type: Type[IQueryHandler]) -> None:
        raise NotImplementedError()

    async def detach_command_handler(self, handler_type: Type[ICommandHandler]) -> None:
        raise NotImplementedError()

    async def on_query(self, query: IQuery) -> Any:
        raise NotImplementedError()

    async def on_command(self, command: ICommand) -> None:
        raise NotImplementedError()
