from asterisk_ng.system.dispatcher import IFunction


__all__ = ["IGenerateLinkFunction"]


class IGenerateLinkFunction(IFunction[str]):

    __slots__ = ()

    async def __call__(self, unique_id: str) -> str:
        raise NotImplementedError()
