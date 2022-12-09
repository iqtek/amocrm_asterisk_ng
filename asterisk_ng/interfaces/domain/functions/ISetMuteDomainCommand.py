from asterisk_ng.system.dispatcher import ICommand

from ...crm_system import CrmUserId


__all__ = ["ISetMuteDomainCommand"]


class ISetMuteDomainCommand(ICommand):

    __slots__ = ()

    async def __call__(
        self,
        user_id: CrmUserId,
        is_mute: bool,
    ) -> None:
        raise NotImplementedError()
