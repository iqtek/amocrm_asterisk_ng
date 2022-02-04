from panoramisk import Manager
from panoramisk.message import Message
from asterisk_amocrm.infrastructure import ILogger
from ...core import (
    Action,
    Response,
    IAmiManager,
    IAmiEventHandler,
    IAmiMessageConvertFunction,
)
from asterisk_amocrm.infrastructure.context_vars import IAddContextVarFunction

__all__ = [
    "AmiManagerImpl",
]


class AmiManagerImpl(IAmiManager):

    def __init__(
        self,
        manager: Manager,
        ami_message_convert_function: IAmiMessageConvertFunction,
        add_context_var_function: IAddContextVarFunction,
        logger: ILogger,
    ) -> None:
        self.__manager = manager
        self.__ami_message_convert_function = ami_message_convert_function
        self.__add_context_var_function = add_context_var_function
        self.__logger = logger

    def connect(self) -> None:
        self.__manager.connect()

    def disconnect(self) -> None:
        self.__manager.close()

    async def send_action(self, action: Action) -> Response:
        response = await self.__manager.send_action(dict(action))
        parameters = dict(response[0])
        parameters.pop("content")
        status = parameters.pop("Response")
        id = parameters.pop("ActionID", None)
        resp = Response(status, parameters, id)
        self.__logger.debug(
            f"AmiManager: send action={action}, response={resp}"
        )
        return resp

    def attach_event_handler(self, event_handler: IAmiEventHandler) -> None:
        self.__attach_event_handler(event_handler)

    def __attach_event_handler(self, event_handler: IAmiEventHandler) -> None:
        async def wrapper(manager: Manager, message: Message) -> None:
            nonlocal event_handler
            self.__add_context_var_function()
            try:
                event = self.__ami_message_convert_function(message)
            except Exception as e:
                self.__logger.error(
                    f"AmiManager: error validation of message: {message}. "
                    f"exc={e!r}"
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
                    f"error calling event handler={event_handler}. exc={e!r}"
                )
        self.__manager.register_event(event_handler.event_pattern(), wrapper)
