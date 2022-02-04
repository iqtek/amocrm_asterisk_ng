from amo_crm_api_client import AmoCrmApiClient
from amo_crm_api_client.exceptions import AmocrmClientException
from asterisk_amocrm.infrastructure import ILogger
from ..core import IRaiseCardCH
from ...commands import RaiseCardCommand


__all__ = [
    "RaiseCardCH",
]


class RaiseCardCH(IRaiseCardCH):

    def __init__(
        self,
        amo_client: AmoCrmApiClient,
        logger: ILogger,
    ) -> None:
        self.__amo_client = amo_client
        self.__logger = logger

    async def __call__(self, command: RaiseCardCommand) -> None:

        try:
            await self.__amo_client.events.add_card(
                phone_number=command.phone_number,
                users=command.users,
            )
        except AmocrmClientException as e:
            self.__logger.error(
                "RaiseCardCH: error raise card "
                "phone_number: '{}' "
                "for users: '{}' .".format(
                    command.phone_number,
                    command.users,
                )
            )
            self.__logger.exception(e)

        self.__logger.debug(
            "RaiseCardCH: raise card "
            "phone_number: '{}' "
            "for users: '{}' .".format(
                command.phone_number,
                command.users,
            )
        )
