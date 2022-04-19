from typing import Collection

from amo_crm_api_client import AmoCrmApiClient
from amo_crm_api_client.exceptions import AmocrmClientException

from amocrm_asterisk_ng.domain import IRaiseCardCommand
from amocrm_asterisk_ng.infrastructure import ILogger


__all__ = [
    "RaiseCardCommand",
]


class RaiseCardCommand(IRaiseCardCommand):

    __slots__ = (
        "__amo_client",
        "__logger",
    )

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        logger: ILogger,
    ) -> None:
        self.__amo_client = amo_client
        self.__logger = logger

    async def __call__(
        self,
        phone_number: str,
        users: Collection[int],
    ) -> None:

        try:
            await self.__amo_client.events.add_card(
                phone_number=phone_number,
                users=users,
            )
        except AmocrmClientException as e:
            self.__logger.error(
                "RaiseCardCommand: error raise card "
                f"phone_number: '{phone_number}' "
                f"for users: '{users}'."
            )
            self.__logger.exception(e)

        self.__logger.debug(
            "RaiseCardCommand: raise card "
            f"phone_number: '{phone_number}' "
            f"for users: '{users}'."
        )
