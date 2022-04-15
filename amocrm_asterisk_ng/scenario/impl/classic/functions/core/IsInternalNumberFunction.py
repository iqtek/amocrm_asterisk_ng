__all__ = [
    "IsInternalNumberFunction",
]


class IsInternalNumberFunction:

    __slots__ = ()

    async def __call__(self, phone_number: str) -> bool:
        raise NotImplementedError
