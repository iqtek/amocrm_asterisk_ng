from .IFunction import IFunction


__all__ = [
    "ICommand",
]


class ICommand(IFunction[None]):

    __slots__ = ()

    async def __call__(self, *args, **kwargs) -> None:
        raise NotImplementedError()
