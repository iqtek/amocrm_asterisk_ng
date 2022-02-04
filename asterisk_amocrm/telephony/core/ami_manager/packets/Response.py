from typing import (
    TypeVar,
    Optional,
    Mapping,
    Type,
)
from .Action import Action
from .Packet import Packet


__all__ = [
    "Response",
]


T = TypeVar("T")


class Response(Packet):

    __slots__ = ()

    _STATUS_KEY = "Response"
    _ID_KEY = "ActionID"

    @classmethod
    def from_action(
        cls: Type[T],
        action: Action,
        status: str,
        parameters: Mapping[str, str] = None,
    ) -> T:
        return cls(status, parameters, action.id)

    def __init__(
        self,
        status: str,
        parameters: Optional[Mapping[str, str]] = None,
        id: Optional[str] = None,
    ) -> None:
        if parameters is None:
            parameters = {}
        else:
            parameters = {**parameters}
        parameters[self._STATUS_KEY] = status
        if id is not None:
            parameters[self._ID_KEY] = id
        super().__init__(parameters)

    @property
    def status(self) -> str:
        return self[self._STATUS_KEY]

    @property
    def id(self) -> Optional[str]:
        return self.get(self._ID_KEY)
