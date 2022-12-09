from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from copy import deepcopy

__all__ = ["AuthMiddleware"]


class AuthMiddleware:

    __slots__ = (
        "__secret_key",
    )

    def __init__(self, secret_key: str = "AsteriskNG") -> None:
        self.__secret_key = secret_key

    async def __call__(self, request: Request, call_next) -> Response:

        if request.url.path != "/asterisk_ng":
            return await call_next(request)

        secret_key = request.query_params.get("secret_key")

        if secret_key is None or secret_key != self.__secret_key:
            return JSONResponse(
                content={
                    "headers": {
                        "status_code": 401,
                        "detail": "Invalid secret key."
                    }
                }
            )
        return await call_next(request)
