from typing import Any
from typing import Generic
from typing import MutableMapping
from typing import Optional
from typing import TypeVar

from .core import IResolver
from .core import Key

from .exceptions import ResolverNotFound
from .exceptions import UnableToResolveDependency


T = TypeVar('T')


class Container(Generic[T]):

    __slots__ = (
        "__resolvers",
    )

    def __init__(self) -> None:
        self.__resolvers: MutableMapping[Key[T], IResolver[T]] = {}

    def set_resolver(self, key: Key[T], resolver: IResolver[T]) -> None:
        self.__resolvers[key] = resolver

    def get_resolver(self, key: Key[T]) -> IResolver[T]:
        return self.__resolvers[key]

    def delete_resolver(self, key: Key) -> None:
        self.__resolvers.pop(key)

    def resolve(self, key: Key[T], needy: Optional[Any] = None) -> T:
        resolver = self.__resolvers[key]
        return resolver(needy=needy)
