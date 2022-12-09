from asterisk_ng.system.dispatcher import ICommand


__all__ = ["IRedirectTelephonyCommand"]


class IRedirectTelephonyCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        phone_number: str,
        redirect_phone_number: str,
    ) -> None:
        raise NotImplementedError()
