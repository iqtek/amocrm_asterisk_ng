from .packets import Event


__all__ = [
    "IAmiEventHandler"
]


class IAmiEventHandler:

    __slots__ = ()

    @classmethod
    def event_pattern(cls) -> str:
        raise NotImplementedError()

    async def __call__(self, event: Event) -> None:
        raise NotImplementedError()
