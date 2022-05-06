from amocrm_asterisk_ng.infrastructure import IFunction


__all__ = [
    "IMakeLinkFunction",
    "MakeLinkFunctionImpl",
]


class IMakeLinkFunction(IFunction[str]):

    __slots__ = ()

    async def __call__(self, unique_id: str) -> str:
        raise NotImplementedError()


class MakeLinkFunctionImpl(IMakeLinkFunction):

    __slots__ = (
        "__base_url",
    )

    def __init__(self, base_url: str) -> None:
        self.__base_url = base_url.rstrip('/')

    async def __call__(self, unique_id: str) -> str:
        return f"{self.__base_url}/amocrm/records/{unique_id}"
