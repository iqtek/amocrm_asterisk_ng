from typing import (
    Optional,
    Mapping,
    Any,
)
from fastapi import (
    Response,
    Request,
)

from asterisk_amocrm.domains import OriginationRequestEvent
from asterisk_amocrm.infrastructure import IEventBus, ILogger
from ..AsteriskWidgetConfig import AsteriskWidgetConfig
from asterisk_amocrm.infrastructure.context_vars import IAddContextVarFunction


__all__ = [
    "OriginationView"
]


class OriginationView:

    def __init__(
        self,
        config: AsteriskWidgetConfig,
        event_bus: IEventBus,
        add_context_var_function: IAddContextVarFunction,
        logger: ILogger
    ) -> None:
        self.__add_context_var_function = add_context_var_function
        self.__config = config
        self.__event_bus = event_bus
        self.__logger = logger

    def __make_response(
        self,
        data: Optional[Mapping[str, Any]] = None
    ) -> Response:
        if not data:
            data = dict()
        response = Response(
            content=f"asterisk_cb({str(data)});",
            media_type="text/javascript"
        )
        return response

    async def handle(self, request: Request) -> Response:

        self.__add_context_var_function()

        self.__logger.warning(
            "OriginationHandler: request: "
            f"{request}"
        )

        request_params = request.query_params
        try:
            login = request_params["_login"]
            password = request_params["_secret"]
            action = request_params["_action"]
        except KeyError:
            self.__logger.warning(
                "OriginationHandler: "
                "Invalid request data."
            )
            return self.__make_response({"status": "invalid data."})

        if login != self.__config.login or password != self.__config.password:
            self.__logger.warning(
                "OriginationHandler: "
                "Attempted request with invalid credentials."
            )
            return self.__make_status_response({"status": "not authorized"})

        if action == "status":
            return self.__make_response({"status": "ok"})

        if action == "call":
            caller_phone_number = request_params["from"]
            called_phone_number = request_params["to"]
            event = OriginationRequestEvent(
                caller_phone_number=caller_phone_number,
                called_phone_number=called_phone_number
            )
            await self.__event_bus.on_event(event)
            return self.__make_response()
