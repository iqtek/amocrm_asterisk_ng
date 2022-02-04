__all__ = [
    'IComponent',
]


class IComponent:

    async def initialize(self) -> None:
        raise NotImplementedError()

    async def deinitialize(self) -> None:
        raise NotImplementedError()
