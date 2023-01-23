from typing import Sequence
from typing import Type

from asterisk_ng.system.dispatcher import IFunction
from pydantic import BaseModel

from asterisk_ng.system.container import Key


__all__ = ["Interface"]


class Interface(BaseModel):
    container: Sequence[Key] = []
    dispatcher: Sequence[Type[IFunction]] = []

    class Config:
        arbitrary_types_allowed = True
