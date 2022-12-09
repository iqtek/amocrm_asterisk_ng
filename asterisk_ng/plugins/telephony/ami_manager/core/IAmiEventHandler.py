from .packets import Event


__all__ = ["IAmiEventHandler"]


class IAmiEventHandler:

    __slots__ = ()

    async def __call__(self, event: Event) -> None:
        raise NotImplementedError()
