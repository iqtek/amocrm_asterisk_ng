from typing import Any
from typing import Mapping


__all__ = [
    "InvalidParamsException",
    "UnknownMethodException",
    "InvalidMethodParamsException",
]


class InvalidParamsException(Exception):
    pass


class UnknownMethodException(Exception):

    __slots__ = ()

    def __init__(self, method: str):
        self.method = method


class InvalidMethodParamsException(Exception):

    __slots__ = ()

    def __init__(self, method: str, params: Mapping[str, Any]):
        self.method = method
        self.params = params
