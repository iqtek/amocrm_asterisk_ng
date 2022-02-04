from .packets import Event


__all__ = [
    "IAmiEventHandler"
]


class IAmiEventHandler:

    @classmethod
    def event_pattern(cls) -> str:
        raise NotImplementedError()

    async def __call__(self, event: Event) -> None:
        raise NotImplementedError()
