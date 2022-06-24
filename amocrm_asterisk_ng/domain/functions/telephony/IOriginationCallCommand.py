from glassio.dispatcher import ICommand


__all__ = [
    "IOriginationCallCommand",
]


class IOriginationCallCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        caller_phone_number: str,
        called_phone_number: str,
    ) -> None:
        """
        Originate a call between two numbers.
        """
        raise NotImplementedError()
