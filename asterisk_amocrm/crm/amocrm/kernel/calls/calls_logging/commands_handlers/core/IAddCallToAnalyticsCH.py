from asterisk_amocrm.infrastructure import ICommandHandler
from ...commands import AddCallToAnalyticsCommand


__all__ = [
    "IAddCallToAnalyticsCH",
]


class IAddCallToAnalyticsCH(ICommandHandler):

    async def __call__(self, command: AddCallToAnalyticsCommand) -> None:
        raise NotImplementedError()
