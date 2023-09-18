import typing as t


__all__ = ["Plugin"]


class Plugin:

    __slots__ = ()

    async def upload(self, settings: t.Mapping[str, t.Any]) -> None:
        raise NotImplementedError()

    async def unload(self) -> None:
        raise NotImplementedError()
