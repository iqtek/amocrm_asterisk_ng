from typing import (
    TypeVar,
    Any,
)
from .IQuery import IQuery


__all__ = [
    "IQueryHandler",
]


Q = TypeVar('Q', bound=IQuery)


class IQueryHandler:

    async def __call__(self, query: Q) -> Any:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return "<{}>".format(self.__class__.__name__)

    def __str__(self) -> str:
        return "{}".format(self.__class__.__name__)
