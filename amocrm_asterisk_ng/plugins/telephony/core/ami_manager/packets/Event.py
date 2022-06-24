from typing import Mapping
from typing import Optional

from .Packet import Packet


__all__ = [
    "Event",
]


class Event(Packet):

    __slots__ = ()

    _NAME_KEY = "Event"
    _ID_KEY = "ActionID"

    def __init__(
        self,
        name: str,
        parameters: Optional[Mapping[str, str]] = None,
        id: Optional[str] = None,
    ) -> None:
        if parameters is None:
            parameters = {}
        else:
            parameters = {**parameters}
        parameters[self._NAME_KEY] = name
        if id is not None:
            parameters[self._ID_KEY] = id
        super().__init__(parameters)

    @property
    def name(self) -> str:
        return self[self._NAME_KEY]

    @property
    def id(self) -> Optional[str]:
        return self.get(self._ID_KEY)
