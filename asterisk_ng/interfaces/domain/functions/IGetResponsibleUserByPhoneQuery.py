from asterisk_ng.system.dispatcher import IQuery


__all__ = ["IGetResponsibleUserByPhoneQuery"]


class IGetResponsibleUserByPhoneQuery(IQuery[str]):

    __slots__ = ()

    async def __call__(self, client_phone: str) -> str:
        raise NotImplementedError()
