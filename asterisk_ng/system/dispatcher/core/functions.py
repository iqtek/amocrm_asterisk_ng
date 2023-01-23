from abc import ABC
from typing import Any
from typing import Generic
from typing import Mapping
from typing import Sequence
from typing import TypeVar


__all__ = [
    "IFunction",
    "ICommand",
    "IQuery",
]


T = TypeVar('T')


class IFunction(Generic[T], ABC):

    __slots__ = ()

    async def __call__(self, *args: Sequence[Any], **kwargs: Mapping[str, Any]) -> T:
        raise NotImplementedError()


class ICommand(IFunction[None], ABC):

    __slots__ = ()


class IQuery(IFunction[T], ABC):

    __slots__ = ()
