from asterisk_ng.system.dispatcher import ICommand


__all__ = ["ISetMuteTelephonyCommand"]


class ISetMuteTelephonyCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        phone_number: str,
        is_mute: bool,
    ) -> None:
        raise NotImplementedError()
