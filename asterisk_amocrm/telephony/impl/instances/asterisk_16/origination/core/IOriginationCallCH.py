from asterisk_amocrm.infrastructure.dispatcher import ICommandHandler
from .OriginationCallCommand import OriginationCallCommand


__all__ = [
    "IOriginationCallCH",
]


class IOriginationCallCH(ICommandHandler):

    async def __call__(self, command: OriginationCallCommand) -> None:
        raise NotImplementedError()
