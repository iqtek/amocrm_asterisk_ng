from typing import Any
from typing import Type
from typing import TypeVar
from typing import Optional
from typing import MutableMapping

from ...core import IRegisteringFactory


__all__ = [
    "RegisteringFactory",
]


T = TypeVar('T')


class RegisteringFactory(IRegisteringFactory[T]):

    __slots__ = (
        "__type_catalog",
    )

    def __init__(self) -> None:
        self.__type_catalog: MutableMapping[str, Type[T]] = {}

    def register_type(
        self,
        type_name: str,
        obj_type: Type[T]
    ) -> None:
        self.__type_catalog[type_name] = obj_type

    def unregister_type(self, type_name: str) -> None:
        self.__type_catalog.pop(type_name)

    def get_instance(self, type_name: str, **kwargs) -> T:
        selected_type = self.__type_catalog.get(type_name)
        if selected_type is None:
            raise KeyError(
                "It is not known which type to instantiate."
            )

        obj = selected_type(**kwargs)
        return obj
