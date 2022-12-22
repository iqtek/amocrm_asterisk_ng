from asyncio import Lock
from asyncio import sleep
from asyncio import create_subprocess_exec

from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Optional

from panoramisk import Manager
from panoramisk import Message

from asterisk_ng.system.components import AbstractInitializableComponent
from asterisk_ng.system.components import InitializedState
from asterisk_ng.system.components import required_state

from asterisk_ng.system.tracing import set_trace_id

from asterisk_ng.system.logger import ILogger
from .message_convert_function import message_convert_function

from ..core import Action
from ..core import IAmiEventHandler
from ..core import IAmiManagerComponent
from ..core import Response


__all__ = ["AmiManagerComponent"]


class AmiManagerComponent(AbstractInitializableComponent, IAmiManagerComponent):

    __slots__ = (
        "__logger",
        "__manager",
        "__lock",
    )

    def __init__(self, manager: Manager, logger: ILogger) -> None:
        super().__init__(name="AmiManagerComponent")
        self.__manager = manager
        self.__logger = logger
        self.__lock = Lock()

    async def __check_connection(self) -> None:
        try:
            self.__manager.ping()
        except Exception as exc:
            raise ConnectionError(
                f"Error of connection to AMI on {self.__manager.config['host']}:{self.__manager.config['port']}."
            ) from exc

    async def _initialize(self) -> None:
        self.__manager.connect()
        await sleep(1.0)
        await self.__check_connection()

    @required_state(InitializedState)
    async def send_action(self, action: Action) -> None:
        try:
            response = await self.__manager.send_action(dict(action))
        except Exception as exc:
            await self.__logger.error(f"Error sending action: `{action}`.", exception=exc)
            raise exc

        await self.__logger.debug(f"Action sent: `{action}`; response: `{response}`.")

    def __wrap_handler(self, event_handler: IAmiEventHandler) -> Callable[[Manager, Message], Coroutine[Any, Any, None]]:
        async def wrapper(manager: Manager, message: Message) -> None:
            nonlocal event_handler
            event = message_convert_function(message)
            async with self.__lock:

                trace_id = event.get("Linkedid", None)

                if trace_id is not None:
                    set_trace_id(trace_id)

                await self.__logger.debug(f"Catch event: `{event}`.")
                try:
                    await event_handler(event)
                except Exception as exc:
                    await self.__logger.error(
                        f"Error calling event handler: `{event_handler}`; event: {event}.",
                        exception=exc,
                    )
        return wrapper

    def attach_event_handler(self, event_pattern: str, event_handler: IAmiEventHandler) -> None:
        wrapped_handler = self.__wrap_handler(event_handler)
        self.__manager.register_event(event_pattern, wrapped_handler)

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        try:
            self.__manager.close()
        except RuntimeError:
            pass  # Fail to send {'Action': 'Ping'}
