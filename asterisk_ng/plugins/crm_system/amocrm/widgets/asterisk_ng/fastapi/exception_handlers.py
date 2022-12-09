from fastapi import Request
from fastapi.responses import JSONResponse

from .exceptions import BadRequest
from .exceptions import IncompatibleVersion

from ..controller import UnknownMethodException
from ..controller import InvalidMethodParamsException


__all__ = [
    "incompatible_version_exception_handler",
    "invalid_method_params_exception_handler",
    "unknown_method_exception_handler",
    "bad_request_exception_handler",
]


async def incompatible_version_exception_handler(request: Request, exc: IncompatibleVersion):
    return JSONResponse(
        content={
            "headers": {
                "status_code": 409,
                "detail": "Incompatible version of the widget."
            }
        }
    )


async def bad_request_exception_handler(request: Request, exc: BadRequest):
    return JSONResponse(
        content={
            "headers": {
                "status_code": 400,
                "detail": "Bad Request."
            }
        }
    )


async def invalid_method_params_exception_handler(request: Request, exc: InvalidMethodParamsException):
    return JSONResponse(
        content={
            "headers":
                {
                    "status_code": "410",
                    "detail": f"Invalid method parameters method: {exc.method}; params: {exc.params}"
                }
        },
    )


async def unknown_method_exception_handler(request: Request, exc: UnknownMethodException):
    return JSONResponse(
        content={
            "headers":
                {
                    "status_code": "404",
                    "detail": f"Unknown method: {exc.method}"
                }
        },
    )
