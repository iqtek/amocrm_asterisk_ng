from asyncio import sleep
from typing import Type

from panoramisk import Manager
from panoramisk.message import Message

from glassio.context import set_context
from glassio.logger import ILogger

from amocrm_asterisk_ng.infrastructure import generate_trace_id

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
        "__handlers",
        "__logger",
    )

    def __init__(
        self,
        manager: Manager,
        ami_message_convert_function: IAmiMessageConvertFunction,
        logger: ILogger,
    ) -> None:
        self.__manager = manager
        self.__ami_message_convert_function = ami_message_convert_function
        self.__handlers: MutableMapping[Type[IAmiEventHandler], IAmiEventHandler] = {}
        self.__logger = logger

    async def __ping(self) -> None:
        for _ in range(10):
            await sleep(1)
            try:
                self.__manager.ping()
                return
            except Exception:
                pass
        raise ConnectionError("AmiManagerImpl: Unable to connect to server.")

    async def connect(self) -> None:
        self.__manager.connect()
        await self.__ping()

    def disconnect(self) -> None:
        self.__manager.close()

    async def send_action(self, action: Action) -> Response:
        try:
            response = await self.__manager.send_action(dict(action))
        except Exception as exc:
            await self.__logger.error(
                f"AmiManager: error sending action: `{action}`.",
                exception=exc,

            )
            raise exc
        parameters = dict(response[0])
        parameters.pop("content")
        status = parameters.pop("Response")
        id = parameters.pop("ActionID", None)
        response = Response(status, parameters, id)
        await self.__logger.debug(
            f"AmiManager: send action: `{action}`; response: `{response}`."
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

            trace_id = generate_trace_id()
            set_context({"trace_id": trace_id})

            try:
                event = self.__ami_message_convert_function(message)
            except Exception as exc:
                await self.__logger.error(
                    f"AmiManager: error validation of message: {message}.",
                    exception=exc
                )
                return
            await self.__logger.debug(
                f"AmiManager: catch event: `{event!r}`."
            )
            try:
                await event_handler(event)
            except Exception as exc:
                await self.__logger.debug(
                    "AmiManager: "
                    f"error calling event handler: `{event_handler}` exc: `{exc!r}`.",
                )
        self.__manager.register_event(event_handler.event_pattern(), wrapper)
