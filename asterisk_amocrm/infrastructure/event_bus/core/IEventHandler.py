from .IEvent import IEvent


__all__ = [
    "IEventHandler",
]


class IEventHandler:

    async def __call__(self, event: IEvent) -> None:
        raise NotImplementedError()
