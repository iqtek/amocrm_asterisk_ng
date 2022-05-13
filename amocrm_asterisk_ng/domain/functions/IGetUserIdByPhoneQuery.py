from glassio.dispatcher import IQuery

from ..models import File


__all__ = [
    "IGetUserIdByPhoneQuery",
]


class IGetUserIdByPhoneQuery(IQuery[int]):

    __slots__ = ()

    async def __call__(self, phone_number: str) -> int:
        raise NotImplementedError()
