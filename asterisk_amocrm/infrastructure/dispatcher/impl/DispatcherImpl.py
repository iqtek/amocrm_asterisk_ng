from collections import (
    defaultdict,
)
from typing import (
    Literal,
    Dict,
    Type,
    Set,
    Any,
)

from asterisk_amocrm.infrastructure.logger import ILogger
from ..core import (
    IDispatcher,
    IQuery,
    ICommand,
    IQueryHandler,
    ICommandHandler,
)

__all__ = [
    "DispatcherImpl"
]


class DispatcherImpl(IDispatcher):
    def __init__(
        self,
        logger: ILogger,
    ) -> None:
        self.__queries:  Dict[Type, Set[IQueryHandler]] = defaultdict(set)
        self.__commands:  Dict[Type, Set[ICommandHandler]] = defaultdict(set)
        self.__logger = logger

    def __attach_handler(
        self,
        handler_species: Literal["query", "command"],
        interface_type,
        handler,
    ) -> None:
        interface_arg_type = interface_type.__call__.__annotations__[handler_species]
        instance_arg_type = handler.__call__.__annotations__[handler_species]
        if not issubclass(type(handler), interface_type):
            raise TypeError(
                "The handler does not implement "
                "the specified interface."
            )
        if not interface_arg_type == instance_arg_type:
            raise TypeError(
                "Interface and implementation "
                "accept different types of queries."
                f"{interface_arg_type} not equal {instance_arg_type}."
            )
        if handler_species == "query":
            mapping = self.__queries
        else:
            mapping = self.__commands

        for instance in mapping[interface_arg_type]:
            if type(instance) == type(handler):
                raise LookupError(
                    f"Handler with type={type(handler)} "
                    f"is already attached."
                )
        mapping[interface_arg_type].add(handler)

    def __detach_handler(
        self,
        handler_species: Literal["query", "command"],
        handler_type: Type,
    ) -> None:

        if handler_species == "query":
            mapping = self.__queries
        else:
            mapping = self.__commands

        event_type = handler_type.__call__.__annotations__[handler_species]

        for instance in mapping[event_type]:
            if handler_type == type(instance):
                fey_handler = instance
                break
        else:
            raise KeyError(
                f"Handler with type={handler_type} "
                f"is not attached."
            )
        mapping[event_type].remove(fey_handler)

    async def attach_query_handler(
        self,
        interface_type: Type,
        query_handler: IQueryHandler
    ) -> None:
        query_type = interface_type.__call__.__annotations__["query"]
        try:
            self.__attach_handler(
                handler_species="query",
                interface_type=interface_type,
                handler=query_handler,
            )
        except Exception as exception:
            self.__logger.error(
                f"Dispatcher: Error of attach QueryHandler: {query_handler} "
                f"for Interface: {interface_type} by query: {query_type}."
            )
            raise exception
        self.__logger.debug(
            f"Dispatcher: Attach QueryHandler: {query_handler} "
            f"on query: {query_type}."
        )

    async def attach_command_handler(
        self,
        interface_type: Type,
        command_handler: ICommandHandler
    ) -> None:
        command_type = interface_type.__call__.__annotations__["command"]
        try:
            self.__attach_handler(
                handler_species="command",
                interface_type=interface_type,
                handler=command_handler,
            )
        except Exception as exception:
            self.__logger.error(
                f"Dispatcher: Error of attach CommandHandler: {command_handler} "
                f"for Interface: {interface_type} by command: {command_type}."
            )
            raise exception
        self.__logger.debug(
            f"Dispatcher: Attach CommandHandler: {command_handler} "
            f"by command: {command_type}."
        )

    async def detach_query_handler(self, handler_type: Type[IQueryHandler]) -> None:
        query_type = handler_type.__call__.__annotations__["query"]
        try:
            self.__detach_handler(
                handler_species="query",
                handler_type=handler_type,
            )
        except Exception as e:
            self.__logger.error(
                f"Dispatcher: Error of detach QueryHandler: {handler_type}."
            )
            raise e
        self.__logger.debug(
            f"Dispatcher:  Detach QueryHandler: {handler_type}"
            f"by query: {query_type}."
        )

    async def detach_command_handler(self, handler_type: Type[ICommandHandler]) -> None:
        command_type = handler_type.__call__.__annotations__["command"]
        try:
            self.__detach_handler(
                handler_species="command",
                handler_type=handler_type,
            )
        except Exception as e:
            self.__logger.error(
                f"Dispatcher: Error of detach CommandHandler: {handler_type}."
            )
            raise e
        self.__logger.debug(
            f"Dispatcher:  Detach CommandHandler: {handler_type}"
            f"by command: {command_type}."
        )

    async def on_query(self, query: IQuery) -> Any:
        query_type = type(query)
        self.__logger.debug(f"Dispatcher: Caught Query: {query}.")
        try:
            handlers = self.__queries[query_type]
        except KeyError as e:
            self.__logger.warning(
                f"Dispatcher: Not found QueryHandler for Query: {query_type}."
            )
            raise e
        for handler in handlers:
            self.__logger.debug(
                f"Dispatcher: QueryHandler called: {handler} "
                f"for query: {query_type}."
            )
            try:
                return await handler(query)
            except Exception as e:
                self.__logger.debug(
                    f"Dispatcher: error of calling QueryHandler: {handler}"
                    f" for query: {query_type}. {e!r}"
                )
                raise e

    async def on_command(self, command: ICommand) -> None:
        command_type = type(command)
        self.__logger.debug(f"Dispatcher: Caught Command: {command}.")
        try:
            handlers = self.__commands[command_type]
            for handler in handlers:
                self.__logger.debug(
                    f"Dispatcher: CommandHandler called: {handler} "
                    f"for command: {command_type}."
                )
                try:
                    await handler(command)
                except Exception as e:
                    self.__logger.debug(
                        f"Dispatcher: Error of calling CommandHandler: {handler}"
                        f"for command: {command_type}. {e}"
                    )
                    raise e
        except KeyError:
            self.__logger.warning(
                f"Dispatcher: Not found CommandHandler for Command: {command_type}."
            )
