from amocrm_asterisk_ng.infrastructure import IQuery

__all__ = [
    "IsUserPhoneNumerQuery",
]


class IsUserPhoneNumerQuery(IQuery[bool]):

    __slots__ = ()

    async def __call__(self, phone_number: str) -> bool:
        raise NotImplementedError()
