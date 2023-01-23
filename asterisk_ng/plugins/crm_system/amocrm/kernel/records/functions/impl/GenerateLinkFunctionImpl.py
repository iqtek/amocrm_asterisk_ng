from ..core import IGenerateLinkFunction


__all__ = ["GenerateLinkFunctionImpl"]


class GenerateLinkFunctionImpl(IGenerateLinkFunction):

    __slots__ = (
        "__base_url",
    )

    def __init__(self, base_url: str) -> None:
        self.__base_url = base_url.rstrip('/')

    async def __call__(self, unique_id: str) -> str:
        return f"{self.__base_url}/records/{unique_id}"
