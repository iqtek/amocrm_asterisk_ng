from amocrm_asterisk_ng.infrastructure import ICommand


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
        raise NotImplementedError()
