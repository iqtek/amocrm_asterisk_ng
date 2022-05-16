from glassio.dispatcher import IQuery


__all__ = [
    "IGetResponsibleUserByPhoneQuery",
]


class IGetResponsibleUserByPhoneQuery(IQuery[str]):

    __slots__ = ()

    async def __call__(self, phone_number: str) -> str:
        raise NotImplementedError()
