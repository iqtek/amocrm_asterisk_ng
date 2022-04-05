from typing import Generic
from typing import Type
from typing import TypeVar


__all__ = [
    "IRegisteringFactory",
]


T = TypeVar('T')


class IRegisteringFactory(Generic[T]):

    __slots__ = ()

    def register_type(
        self,
        type_name: str,
        obj_type: Type[T]
    ) -> None:
        """Register object type by string name."""
        raise NotImplementedError()

    def unregister_type(
        self,
        type_name: str,
    ) -> None:
        """
        Unregister object type by string name.

        :raise KeyError: If the type has not been registered.
        """
        raise NotImplementedError()

    def get_instance(self, type_name: str, **kwargs) -> T:
        """
        Create an object of the selected type.

        :raise KeyError: If the type has not been registered.
        :raise Exception: If unable to create event from content.
        """
        raise NotImplementedError()
