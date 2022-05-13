from glassio.dispatcher import IQuery


__all__ = [
    "IGetPhoneByUserIdQuery",
]


class IGetPhoneByUserIdQuery(IQuery[str]):

    __slots__ = ()

    async def __call__(self, user_id: int) -> str:
        """Get user  hone number by his id."""
        raise NotImplementedError()
