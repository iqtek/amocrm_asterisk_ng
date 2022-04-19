__all__ = [
    "IScenario",
]


class IScenario:

    async def upload(self) -> None:
        raise NotImplementedError()

    async def unload(self) -> None:
        raise NotImplementedError()
