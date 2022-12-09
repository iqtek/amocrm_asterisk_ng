from .IKeyValueStorage import IKeyValueStorage


__all__ = ["IKeyValueStorageFactory"]


class IKeyValueStorageFactory:

    __slots__ = ()

    def __call__(self, prefix: str = None) -> IKeyValueStorage:
        raise NotImplementedError()
