from typing import Any
from typing import Mapping
from typing import Optional

from fastapi import Request
from fastapi import Response
from glassio.logger import ILogger

from amocrm_asterisk_ng.domain import IOriginationRequestCommand

from .AsteriskWidgetConfig import AsteriskWidgetConfig


__all__ = [
    "WidgetView"
]


class WidgetView:

    __slots__ = (
        "__config",
        "__origination_request_command",
        "__logger",
    )

    def __init__(
        self,
        config: AsteriskWidgetConfig,
        origination_request_command: IOriginationRequestCommand,
        logger: ILogger
    ) -> None:
        self.__origination_request_command = origination_request_command
        self.__config = config
        self.__logger = logger

    def __make_response(
        self,
        data: Optional[Mapping[str, Any]] = None
    ) -> Response:
        data = data or {}
        response = Response(
            content=f"asterisk_cb({str(data)});",
            media_type="text/javascript",
        )
        return response

    async def handle(self, request: Request) -> Response:
        request_params = request.query_params
        print(request.headers)
        try:
            login = request_params["_login"]
            password = request_params["_secret"]
            action = request_params["_action"]
        except KeyError:
            return self.__make_response({"status": "invalid data."})

        if login != self.__config.login or password != self.__config.password:
            await self.__logger.info(
                "Widget: "
                "Attempted request with invalid credentials."
            )
            return self.__make_status_response({"status": "not authorized."})

        if action == "status":
            return self.__make_response({"status": "ok"})

        if action == "cdr":
            return self.__make_response({"status": "no cdr."})

        if action == "call":
            try:
                caller_phone_number = request_params["from"]
                called_phone_number = request_params["to"]
            except KeyError:
                return self.__make_response({"status": "invalid data."})

            await self.__origination_request_command(
                caller_phone_number=caller_phone_number,
                called_phone_number=called_phone_number,
            )

            return self.__make_response()

        return self.__make_response({"status": "unknown action."})
