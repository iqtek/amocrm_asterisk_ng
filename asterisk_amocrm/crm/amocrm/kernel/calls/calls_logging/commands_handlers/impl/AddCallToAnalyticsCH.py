from amo_crm_api_client import AmoCrmApiClient
from amo_crm_api_client.exceptions import AmocrmClientException

from asterisk_amocrm.infrastructure import ILogger
from ..core import IAddCallToAnalyticsCH
from ...commands import AddCallToAnalyticsCommand


__all__ = [
    "AddCallToAnalyticsCH",
]


class AddCallToAnalyticsCH(IAddCallToAnalyticsCH):

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        logger: ILogger,
    ) -> None:
        self.__amo_client = amo_client
        self.__logger = logger

    async def __call__(self, command: AddCallToAnalyticsCommand) -> None:

        try:
            await self.__amo_client.calls.add(
                **command.dict(),
            )
        except AmocrmClientException as e:
            self.__logger.debug(
                "AddCallToAnalyticsCH: "
                "unable to add a call to analytics"
                f" contact '{command.phone}' missing."
            )
            self.__logger.exception(e)
            raise Exception() from e

        self.__logger.debug(
            "AddCallToAnalyticsCH: "
            "call added to analytics"
            f"responsible_user '{command.responsible_user_id}' "
            f"phone '{command.phone}' ."
        )
