from amo_crm_api_client import AmoCrmApiClient
from amo_crm_api_client.exceptions import AmocrmClientException

from asterisk_amocrm.infrastructure import ILogger
from ..core import IAddCallToUnsortedCH
from ...commands import AddCallToUnsortedCommand


__all__ = [
    "AddCallToUnsortedCH",
]


class AddCallToUnsortedCH(IAddCallToUnsortedCH):

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        logger: ILogger,
    ) -> None:
        self.__amo_client = amo_client
        self.__logger = logger

    async def __call__(self, command: AddCallToUnsortedCommand) -> None:

        try:
            await self.__amo_client.unsorted.add_call(
                **command.dict()
            )
        except AmocrmClientException as e:
            self.__logger.debug(
                "AddCallToUnsortedCH: "
                "unable add call to unsorted "
                f"caller: '{command.caller}' "
                f"called: '{command.called}' ."
            )
            self.__logger.exception(e)
            raise Exception() from e

        self.__logger.debug(
            "AddCallToUnsortedCH: "
            "call added to unsorted "
            f"caller: '{command.caller}' "
            f"called: '{command.called}' ."
        )
