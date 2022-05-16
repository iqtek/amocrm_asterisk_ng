from glassio.dispatcher import ICommand


__all__ = [
    "IOriginationRequestCommand",
]


class IOriginationRequestCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        caller_phone_number: str,
        called_phone_number: str,
    ) -> None:
        raise NotImplementedError()
