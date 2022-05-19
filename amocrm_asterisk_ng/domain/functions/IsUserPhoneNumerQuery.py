from glassio.dispatcher import IQuery


__all__ = [
    "IsUserPhoneNumerQuery",
]


class IsUserPhoneNumerQuery(IQuery[bool]):

    __slots__ = ()

    async def __call__(self, phone_number: str) -> bool:
        """
        Check that the number belongs to one of the operators.
        """
        raise NotImplementedError()
