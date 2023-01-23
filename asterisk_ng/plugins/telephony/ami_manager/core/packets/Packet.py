from typing import Mapping

from multidict import CIMultiDict
from multidict import CIMultiDictProxy


__all__ = ["Packet"]


class Packet(CIMultiDictProxy):

    __slots__ = ()

    def __init__(self, parameters: Mapping[str, str]) -> None:
        super().__init__(CIMultiDict(parameters))
