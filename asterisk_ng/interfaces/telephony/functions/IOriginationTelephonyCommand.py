from asterisk_ng.system.dispatcher import ICommand


__all__ = ["IOriginationTelephonyCommand"]


class IOriginationTelephonyCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        caller_phone_number: str,
        called_phone_number: str,
    ) -> None:
        raise NotImplementedError()
