from .Version import Version


__all__ = [
    "IGetCurrentAppVersionFunction",
]


class IGetCurrentAppVersionFunction:

    __slots__ = ()

    def __call__(self) -> Version:
        raise NotImplementedError()
