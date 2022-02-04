from asterisk_amocrm.infrastructure import ICommandHandler
from ...commands import AddCallToUnsortedCommand


__all__ = [
    "IAddCallToUnsortedCH",
]


class IAddCallToUnsortedCH(ICommandHandler):

    async def __call__(self, command: AddCallToUnsortedCommand) -> None:
        raise NotImplementedError()
