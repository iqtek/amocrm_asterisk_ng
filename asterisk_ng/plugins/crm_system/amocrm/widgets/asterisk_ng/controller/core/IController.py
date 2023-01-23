from fastapi import Form
from fastapi.responses import JSONResponse

from .IControllerMethod import IControllerMethod


__all__ = [
    "IController",
]


class IController:

    __slots__ = ()

    def add_method(self, method_name: str, method: IControllerMethod) -> None:
        raise NotImplementedError()

    async def handle(self, json: str = Form()) -> JSONResponse:
        raise NotImplementedError()
