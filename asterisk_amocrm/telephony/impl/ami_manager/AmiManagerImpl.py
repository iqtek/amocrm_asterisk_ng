import asyncio
from typing import Type
from panoramisk import Manager
from panoramisk.message import Message

from asterisk_amocrm.infrastructure import ILogger
from asterisk_amocrm.infrastructure.context_vars import ISetContextVarsFunction

from ...core import Action
from ...core import IAmiEventHandler
from ...core import IAmiManager
from ...core import IAmiMessageConvertFunction
from ...core import Response


__all__ = [
    "AmiManagerImpl",
]


class AmiManagerImpl(IAmiManager):

    __slots__ = (
        "__manager",
        "__ami_message_convert_function",
        "__set_context_vars_function",
        "__handlers",
        "__logger",
    )

    def __init__(
        self,
        manager: Manager,
        ami_message_convert_function: IAmiMessageConvertFunction,
        set_context_vars_function: ISetContextVarsFunction,
        logger: ILogger,
    ) -> None:
        self.__manager = manager
        self.__ami_message_convert_function = ami_message_convert_function
        self.__set_context_vars_function = set_context_vars_function
        self.__handlers: MutableMapping = {}
        self.__logger = logger

    async def connect(self) -> None:
        self.__manager.connect()
        for _ in range(10):
            await asyncio.sleep(1)
            try:
                self.__manager.ping()
                return
            except Exception:
                pass
        raise ConnectionError("AmiManagerImpl: Unable to connect to server.")

    def disconnect(self) -> None:
        self.__manager.close()

    async def send_action(self, action: Action) -> Response:
        try:
            response = await self.__manager.send_action(dict(action))
        except Exception as e:
            self.__logger.warning(
                f"AmiManager: error sending action: {action}. {e}"
            )
            raise e
        parameters = dict(response[0])
        parameters.pop("content")
        status = parameters.pop("Response")
        id = parameters.pop("ActionID", None)
        response = Response(status, parameters, id)
        self.__logger.debug(
            f"AmiManager: send action: {action}; response: {response}."
        )
        return response

    def attach_event_handler(self, event_handler: IAmiEventHandler) -> None:
        self.__handlers[type(event_handler)] = event_handler
        self.__attach_event_handler(event_handler)

    def detach_event_handler(self, handler_type: Type[IAmiEventHandler]) -> None:
        self.__handlers.pop(handler_type)

    def __attach_event_handler(self, event_handler: IAmiEventHandler) -> None:
        async def wrapper(manager: Manager, message: Message) -> None:
            nonlocal event_handler
            if type(event_handler) not in self.__handlers.keys():
                return
            self.__set_context_vars_function()
            try:
                event = self.__ami_message_convert_function(message)
            except Exception as e:
                self.__logger.error(
                    f"AmiManager: error validation of message: {message}. {e}"
                )
                return
            self.__logger.debug(
                f"AmiManager: catch event {event} ."
            )
            try:
                await event_handler(event)
            except Exception as e:
                self.__logger.warning(
                    "AmiManager: "
                    f"error calling event handler: '{event_handler}'. {e}"
                )

        self.__manager.register_event(event_handler.event_pattern(), wrapper)
