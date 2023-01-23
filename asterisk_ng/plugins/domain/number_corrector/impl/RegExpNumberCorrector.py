from re import sub
from re import compile
from ..core import INumberCorrector


__all__ = ["RegExpNumberCorrector"]


class RegExpNumberCorrector(INumberCorrector):

    __slots__ = (
        "__pattern",
        "__replacement",
    )

    def __init__(self, pattern: str, replacement: str) -> None:
        self.__pattern = compile(pattern)
        self.__replacement = replacement

    def correct(self, phone: str) -> str:
        return sub(self.__pattern, self.__replacement, phone)
