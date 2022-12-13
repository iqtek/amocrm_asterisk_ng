import re
from re import compile
from ..core import INumberCorrector


__all__ = ["RegExpNumberCorrector"]


class RegExpNumberCorrector(INumberCorrector):

    __slots__ = (
        "__pattern",
        "__replacement",
    )

    def __init__(self, pattern: str, replacement: str) -> None:
        self.__pattern = pattern
        self.__replacement = replacement

    def correct(self, phone: str) -> str:
        return re.sub(self.__pattern, self.__replacement, phone)
