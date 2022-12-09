from asterisk_ng.system.dispatcher import ICommand

from ...crm_system import CrmUserId


__all__ = ["IHangupDomainCommand"]


class IHangupDomainCommand(ICommand):

    __slots__ = ()

    async def __call__(self, user_id: CrmUserId) -> None:
        raise NotImplementedError()
