from typing import Any
from typing import Mapping
from typing import MutableMapping
from typing import Optional

from fastapi import Form
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from ujson import loads

from asterisk_ng.system.logger import ILogger

from .models import Command, Headers

from ..core import IControllerMethod
from ..core import InvalidMethodParamsException
from ..core import InvalidParamsException
from ..core import UnknownMethodException

from ...fastapi.exceptions import BadRequest
from ...fastapi.exceptions import IncompatibleVersion


__all__ = ["ControllerImpl"]


class ControllerImpl:

    __slots__ = (
        "__methods",
        "__logger",
    )

    def __init__(
        self,
        logger: ILogger,
    ) -> None:
        self.__methods: MutableMapping[str, IControllerMethod] = {}
        self.__logger = logger

    def add_method(self, method_name: str, method: IControllerMethod) -> None:
        self.__methods[method_name] = method

    async def handle(self, json: str = Form()) -> JSONResponse:
        try:
            body = loads(json)

            json_headers = body.get("headers") or {}
            json_content = body.get("content") or {}

            headers = Headers(**json_headers)
            command = Command(**json_content)

        except (KeyError, ValidationError):
            raise BadRequest()

        # Checking version compatibility.

        try:
            major = int(headers.widget_version.split('.')[0])
        except ValueError:
            raise IncompatibleVersion()

        if major != 1:
            raise IncompatibleVersion()

        try:
            method = self.__methods[command.method]
        except KeyError:
            raise UnknownMethodException(command.method)

        try:
            result = await method(headers.amouser_email, headers.amouser_id, **command.params)
        except TypeError as exc:
            await self.__logger.error(
                f"Invalid method parameters. ",
                exception=exc,
            )
            raise InvalidMethodParamsException(command.method, command.params)
        except InvalidParamsException as exc:
            await self.__logger.error(f"Invalid method parameters. ", exc)
        except Exception as exc:
            exc_name = exc.__class__.__name__
            await self.__logger.error(f"Unknown controller method error.", exc)
            response = self.__make_response_with_exception(exc_name, command_id=command.id)
            return response
        else:
            response = self.__make_response_with_result(result, command_id=command.id)
            # await self.__logger.debug(f"Controller method result: `{result}` command: `{command}`.")
            return response

    def __make_response_with_result(self, result: Optional[Mapping[str, Any]], command_id: int) -> JSONResponse:
        response = {
            "headers": {
                "status_code": 200,
                "detail": "success"
            },
            "content": {
                "jsonrpc": "2.0",
                "result": {
                    "result": result,
                },
                "id": command_id,
            }
        }
        return JSONResponse(response)

    def __make_response_with_exception(self, exception: str, command_id: int) -> JSONResponse:
        response = {
            "headers": {
                "status_code": 200,
                "detail": "success"
            },
            "content": {
                "jsonrpc": "2.0",
                "result": {
                    "exception_name": exception,
                },
                "id": command_id,
            }
        }
        return JSONResponse(response)
