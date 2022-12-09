from asterisk_ng.system.dispatcher import ICommand


__all__ = ["IHangupTelephonyCommand"]


class IHangupTelephonyCommand(ICommand):

    __slots__ = ()

    async def __call__(self, phone_number: str) -> None:
        raise NotImplementedError()
