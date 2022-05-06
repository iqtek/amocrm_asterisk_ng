from typing import Any
from typing import Generic
from typing import Mapping
from typing import TypeVar
from typing import Optional


__all__ = [
    "IFactory"
]


T = TypeVar('T')


class IFactory(Generic[T]):

    __slots__ = ()

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> T:
        raise NotImplementedError()
