from typing import Mapping
from typing import Optional
from uuid import uuid4

from .Packet import Packet


__all__ = ["Action"]


class Action(Packet):

    __slots__ = ()

    _NAME_KEY = "Action"
    _ID_KEY = "ActionID"

    def __init__(
        self,
        name: str,
        parameters: Optional[Mapping[str, str]] = None,
        id: Optional[str] = None,
    ) -> None:
        if id is None:
            id = str(uuid4())
        if parameters is None:
            parameters = {}
        else:
            parameters = {**parameters}
        parameters[self._NAME_KEY] = name
        parameters[self._ID_KEY] = id
        super().__init__(parameters)

    @property
    def name(self) -> str:
        return self[self._NAME_KEY]

    @property
    def id(self) -> str:
        return self[self._ID_KEY]
