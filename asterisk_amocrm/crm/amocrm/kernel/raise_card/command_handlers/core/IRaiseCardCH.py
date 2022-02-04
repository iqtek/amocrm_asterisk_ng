from asterisk_amocrm.infrastructure.dispatcher import ICommandHandler
from ...commands import RaiseCardCommand


__all__ = [
    "IRaiseCardCH",
]


class IRaiseCardCH(ICommandHandler):

    async def __call__(self, command: RaiseCardCommand) -> None:
        raise NotImplementedError()
